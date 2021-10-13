"""
Alex Eidt

Creates an acyclic directed graph representing the structure any directory
that is in the same directory as this script.
"""


import os
import json
import argparse
from graphviz import Digraph
from typing import Union

# Change PATH setup for Graphviz directory here:
# --------------------------GRAPHVIZ PATH SETUP------------------------- #
os.environ['PATH'] += os.pathsep + 'C:\\Graphviz\\bin'
# ---------------------------------------------------------------------- #


def convert(size: int) -> str:
    """
    Converts the given "size" into its corresponding bytes representation
    rounded to two decimal places.
    """
    kilo = 1024
    sizes = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    index = 0
    while int(size / kilo) > 0:
        size /= kilo
        index += 1
    suffix = sizes[index]
    if index == 0 and size == 1:
        suffix = 'byte'

    return f'{round(size, 2)} {suffix}'


def size(path: str) -> dict:
    """
    Recursively calculates the size of all files in the given "path"
    directory in an efficient way by starting at the bottom of the directory
    and building up directory sizes. 
    
    Returns a dictionary mapping directory paths to their memory footprint.
    """
    file_sizes = {}
    for root, dirs, files in os.walk(os.path.normpath(f'./{path}/'), topdown=False):
        size = sum([os.path.getsize(os.path.join(root, f)) for f in files])
        file_sizes[root] = size

        for dir_ in dirs:
            path = os.path.join(root, dir_)
            if path in file_sizes:
                file_sizes[root] += file_sizes[path]

    # Convert all sizes in bytes to bytes, MB, GB, etc.
    for path, size in file_sizes.items():
        file_sizes[path] = convert(size)
    
    return file_sizes


def graph_dir(
    directory:      str,
    orientation:    str = 'LR',
    data:           bool = False,
    show_files:     bool = True,
    show_hidden:    bool = False,
    max_depth:      int = -1,
    ranksep:        Union[float, None] = None,
    file_type:      str = 'svg'
) -> None:
    """
    Creates an acyclic directed adjacency graph of the given directory.

    file_name:      The name of the png file that will store the graph
                    representing the directory. Default is the parent directory
                    name.
    directory:      The directory to generate the graph for. Default is '.'.
                    Throws AssertionError if directory is not in the current directory.
    orientation:    Which direction the graph should be drawn in. Options:
                        -LR: Left to Right
                        -RL: Right to Left
                        -TB: Top to Bottom
                        -BT: Bottom to Top
                    Throws AssertionError if "orientation" value is not one of the above.
    data:           If True, shows memory used for each directory and all files in a directory.
    show_files:     If True, shows files that are part of the directory.
    show_hidden:    If True, include hidden directories/objects in the visualization.
    max_depth:      The maximum length of the directory "tree" branches that are created. Useful for
                    large directories with many levels of subfolders if you want to limit the
                    visualization to only the first few layers.
    ranksep:        Distance between "layers" of directories in inches.
    file_type:      File type to render graph as.
    """
    assert directory in os.listdir(), f'Invalid argument for "directory". {directory} is not in the current directory'
    options = ['LR', 'RL', 'TB', 'BT']
    assert orientation.upper() in options, f'Invalid argument for "orientation". Must be one of {", ".join(options)}'
    assert file_type in ['svg', 'png'], 'Invalid argument for "file_type". Must be either "png" or "svg"'

    options = {'rankdir': orientation.upper(), 'overlap': 'scale', 'splines': 'polyline'}
    if ranksep is not None:
        options['ranksep'] = str(ranksep)

    tree = Digraph(graph_attr = options)
    index = 0
    multiple = lambda l: '' if l == 1 else 's'

    # Get data for size of each folder
    if data:
        dir_sizes = size(directory)

    walkdir = os.path.normpath(f'./{directory}/')
    # directory_data is the string used to build up the text in the nodes.
    directory_data = []
    # file_node is the string used to build file information up the text in the nodes.
    file_node = []
    for root, dirs, files in os.walk(walkdir):
        if max_depth > 0 and root.count(os.sep) >= max_depth:
            continue
        if not show_hidden:
            dirs[:] = [dir_ for dir_ in dirs if not dir_.startswith(('__', '.'))]
        tree.attr('node', shape='folder', fillcolor='lemonchiffon', style='filled,bold')

        parent_directory = directory if root == '.' else root
        directory_data.clear()
        directory_data.extend(os.path.basename(parent_directory))
        
        file_memory = convert(sum([os.path.getsize(os.path.join(root, f)) for f in files]))
        # Display directory data if parameters permit
        if data:
            directory_data.extend(f' ({dir_sizes[root]})')
        # \l left aligns items in their container
        directory_data.append('\l')
        if data and dirs:
            directory_data.extend(f'{len(dirs)} Folder{multiple(len(dirs))}\l')
        if data and files:
            directory_data.extend(f'{len(files)} File{multiple(len(files))}')
            if not show_files and dirs:
                directory_data.extend(f' ({file_memory})')
            directory_data.append('\l')

        tree.node(root, label=''.join(directory_data))
        for dir_ in dirs:
            path = os.path.join(root, dir_)
            tree.node(path, label=dir_)
            tree.edge(root, path)

        if files and show_files:
            index += 1
            tree.attr('node', shape='box', style='')
            # Display files in a box on the graph as well as memory information
            # if parameters permit
            if data:
                file_node.extend(f'{len(files)} File{multiple(len(files))} ({file_memory})\l')
            file_node.extend(('\l'.join(files), '\l'))
            file_node_str = ''.join(file_node)
            file_node.clear()
            id_ = f'{index}{file_node_str}'
            tree.node(id_, label=file_node_str)
            tree.edge(root, id_)

    tree.render(f'{directory}_Graph', view=True, format=file_type)
    os.remove(f'{directory}_Graph')


def introduction():
    """
    Introduces the user to the program on the command line and helps them customize their
    parameters for creating the graph.
    """
    print('Welcome to the Directory Grapher!\n')
    print('Enter a directory name that is in this directory. Valid directory names are given below: ')
    valid = set()
    for directory in os.listdir():
        if os.path.isdir(directory):
            print('\t', directory)
            valid.add(directory)
    directory_name = input('directory Name: ')
    while directory_name not in valid:
        directory_name = input(f'{directory_name} is not in the directory. Please enter a new directory name: ')

    depth = input('\nEnter Maximum Directory Depth. Must be an integer. (Enter/Return for no limit): ')
    while depth and not depth.isdigit():
        depth = input('Invalid Depth value. Must be an integer. Please enter again (Enter/Return for no limit): ')
    hidden = input('Would you like to include hidden directories (starting with "." or "__") in the visualization? (y/n): ').lower()
    data = input('Show number of files/directories and memory use for each directory? (y/n): ').lower()
    show_files = input('Show files in each directory? (y/n): ').lower()
    file_type = input('File Type (png or svg): ').lower()
    ranksep = input('Distance between "layers" of directories in inches (Enter/Return for Default): ')
    print('How should the graph be oriented? ')
    print('Top -> Bottom: TB\nBottom -> Top: BT\nLeft -> Right: LR\nRight -> Left: RL')
    orientation = input('Choose one of the options above and enter here: ').upper()

    while orientation not in ['TB', 'BT', 'LR', 'RL']:
        orientation = input('Invalid orientation. Please enter again: ')

    graph_dir(
        directory_name,
        orientation=orientation,
        data=data == 'y',
        show_files=show_files == 'y',
        show_hidden=hidden == 'y',
        max_depth=int(depth) if depth else -1,
        ranksep=float(ranksep) if ranksep else None,
        file_type=file_type
    )

    print(f'\nThe directory graph ({directory_name}_Graph.png) has been created in this directory.')


def main():
    parser = argparse.ArgumentParser(description='Visualizes directory structure with graphs.')
    parser.add_argument('dir', help='Directory Name.')
    parser.add_argument('-i', required=False, help='Use console interface instead of command line args.', action='store_true')
    parser.add_argument('-d', required=False, help='Visualization Depth.')
    parser.add_argument('-hidden', required=False, help='Include hidden directories (starting witih "." or "__").', action='store_true')
    parser.add_argument('-m', required=False, help="Show number of files/dirs and memory use.", action='store_true')
    parser.add_argument('-f', required=False, help='Show files in each directory.', action='store_true')
    parser.add_argument('-o', required=False, help='Graph orientation. Either TB, BT, LR, RL.')
    parser.add_argument('-rs', required=False, help='Distance between "layers" of directories in inches.')
    parser.add_argument('-ft', required=False, help='File Format to render graph as either "svg" or "png".')

    args = parser.parse_args()
    if not args.i:
        graph_dir(
            args.dir,
            orientation=args.o if args.o else 'TB',
            data=bool(args.m),
            show_files=bool(args.f),
            show_hidden=bool(args.hidden),
            max_depth=int(args.d) if args.d else -1,
            ranksep=float(args.rs) if args.rs else None,
            file_type=args.ft if args.ft and args.ft in ['png', 'svg'] else 'svg'
        )
    else:
        introduction()
    

if __name__ == '__main__':
    # Feel free to remove the introduction() function call and replace with
    # whatever code you need. Example function call for creating a graph is
    # shown below:
    #
    # graph_dir(
    #     directory,
    #     orientation='LR',
    #     data=False,
    #     show_files=True,
    #     show_hidden=False,
    #     max_depth=-1,
    #     ranksep=None,
    #     file_type='svg'
    # )

    main()