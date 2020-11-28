"""
Alex Eidt

Creates an acyclic directed graph representing the structure any directory
that is in the same directory as this script.
"""


import os
import json
from graphviz import Digraph

# Change PATH setup for Graphviz directory here:
# --------------------------GRAPHVIZ PATH SETUP------------------------- #
os.environ['PATH'] += os.pathsep + 'C:\\Graphviz\\bin'
# ---------------------------------------------------------------------- #


def size(path):
    """
    Recursively calculates the size of all files in the given "path"
    directory. Returns this size in its corresponding bytes representation.
    """
    size = 0
    for root, dirs, files in os.walk(path):
        size += sum([os.path.getsize(os.path.join(root, f)) for f in files])
    
    return convert(size)


def convert(size):
    """
    Converts the given "size" into its corresponding bytes representation
    rounded to two decimal places.
    """
    kilo = 2 ** 10
    sizes = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    index = 0
    while int(size / kilo) > 0:
        size /= kilo
        index += 1
    if index == 0 and size == 1:
        sizes[index] = 'byte'

    return f'{round(size, 2)} {sizes[index]}'


def main(directory, orientation='LR', data=False, show_files=True):
    """
    Creates an acyclic directed adjacency graph of the given directory.

    file_name: The name of the png file that will store the graph
               representing the directory. Default is the parent directory
               name.

    directory: The directory to generate the graph for. Default is '.'.
            Throws AssertionError if directory is not in the current directory.

    orientation: Which direction the graph should be drawn in. Options:
                 -LR: Left to Right
                 -RL: Right to Left
                 -TB: Top to Bottom
                 -BT: Bottom to Top
                 Throws AssertionError if "orientation" value is not one of the above.
    
    data: If True, shows memory used for each directory and all files in a directory.
    show_files: If True, shows files that are part of the directory.
    """
    assert directory in os.listdir(), f'Invalid argument for "directory". {directory} is not in the current directory'
    options = ['LR', 'RL', 'TB', 'BT']
    assert orientation.upper() in options, f'Invalid argument for "orientation". Must be one of {", ".join(options)}'
    del options

    tree = Digraph(
        graph_attr = {'rankdir': orientation.upper(), 'overlap': 'scale'},
    )
    index = 0
    multiple = lambda l: '' if l == 1 else 's'

    for root, dirs, files in os.walk(os.path.normpath(f'./{directory}/')):
        tree.attr('node', shape='folder', fillcolor='lemonchiffon', style='filled,bold')

        # \l left aligns items in their container
        parent_directory = root
        if root == '.':
            parent_directory = directory
        directory_data = os.path.basename(parent_directory)
        
        # Display directory data if parameters permit
        if data:
            directory_data += f' ({size(root)})'
        directory_data += '\l'
        if data and dirs:
            directory_data += f'{len(dirs)} Folder{multiple(len(dirs))}\l'
        if data and files:
            directory_data += f'{len(files)} File{multiple(len(files))}'
            if not show_files:
                directory_data += f' ({convert(sum([os.path.getsize(os.path.join(root, f)) for f in files]))})'
            directory_data += '\l'

        tree.node(root, label=directory_data)
        for dir_ in dirs:
            path = os.path.join(root, dir_)
            tree.node(path, label=dir_)
            tree.edge(root, path)
        if files and show_files:
            index += 1
            tree.attr('node', shape='box', style='')
            # Display files in a box on the graph as well as memory information
            # if parameters permit
            file_list = '\l'.join(files) + '\l'
            file_node = ''
            if data:
                file_node = f'{len(files)} File{multiple(len(files))}'
                memory_ = f'({convert(sum([os.path.getsize(os.path.join(root, f)) for f in files]))})'
                file_node += f' {memory_}\l'
            file_node += file_list
            id_ = f'{index}{file_node}'
            tree.node(id_, label=file_node)
            tree.edge(root, id_)

    tree.render(f'{directory}_Graph', view=True, format='png')
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

    data = input('Show number of files/directories and memory use for each directory? (y/n): ').lower()
    show_files = input('Show files in each directory? (y/n): ').lower()
    print('How should the graph be oriented? ')
    print('Top -> Bottom: TB\nBottom -> Top: BT\nLeft -> Right: LR\nRight -> Left: RL')
    orientation = input('Choose one of the options above and enter here: ').upper()

    while orientation not in ['TB', 'BT', 'LR', 'RL']:
        orientation = input('Invalid orientation. Please enter again: ')

    main(directory_name, orientation=orientation, data=data == 'y', show_files=show_files == 'y')

    print(f'\nThe directory graph ({directory_name}_Graph.png) has been created in this directory.')


if __name__ == '__main__':
    # Feel free to remove the introduction() function call and replace with
    # whatever code you need. Example function call for creating a graph is
    # shown below:
    #
    # main(directory_name, orientation=orientation, data=True, show_files=True)

    introduction()