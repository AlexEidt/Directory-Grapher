# Directory Grapher

Create acyclic directed graphs representing any directory of your choosing.

## Usage

Run `graph_dir.py` in a directory that contains directories you'd like to visualize. Replace `DIRECTORY_LOCATION_HERE` with the file path to the directory you've chosen.

```
cd DIRECTORY_LOCATION_HERE
python graph_dir.py
```

Once you enter the command above you'll see several prompts. An example is shown below when `graph_dir.py` is run in this directory.

```
Welcome to the Directory Grapher!

Enter a directory name that is in this directory. Valid directory names are given below:
         .vscode
         Demo
Directory Name: Demo
Show number of files/directories and memory use for each directory? (y/n): n
Show files in each directory? (y/n): y
How should the graph be oriented?
Top -> Bottom: TB
Bottom -> Top: BT
Left -> Right: LR
Right -> Left: RL
Choose one of the options above and enter here: RL

The directory graph (Demo_Graph.png) has been created in this directory.
```

As you'll see in the log above, there are several options to customize the graph that is created. It's possible to show data for each directory (the number of sub-directories and files in that directory, as well as the memory use of each file and directory). The user may also choose to show or hide the files in each directory. The user may also choose the orientation of the graph, whether it should start at the bottom and go up, start at the top and go down, start left and go right, or start right and go left.

### Options

*Demo Graph with Data and Files Shown* | Demo Graph with only Data shown
:---: | :---:
<img src="Documentation/Demo_Graph_Data_Files.png" alt="Demo Graph with Data and Files Shown" /> | <img src="Documentation/Demo_Graph_Data.png" alt="Demo Graph with only Data Shown" />
**Demo Graph with only Files Shown** | **Demo Graph with neither Data or Files Shown**
<img src="Documentation/Demo_Graph_Files.png" alt="Demo Graph with only Files Shown" /> | <img src="Documentation/Demo_Graph_Data_BT.png" alt="Demo Graph with neither Data or Files Shown" />

### Orientations

Note that all combinations of parameters are compatible with all combinations of orientations.

Bottom to Top | Top to Bottom
:---: | :---:
<img src="Documentation/Demo_Graph_BT.png" alt="Demo Graph Bottom to Top" /> | <img src="Documentation/Demo_Graph_TB.png" alt="Demo Graph Top to Bottom" />
**Left to Right** | **Right to Left**
<img src="Documentation/Demo_Graph_LR.png" alt="Demo Graph Left to Right" /> | <img src="Documentation/Demo_Graph_Data_RL.png" alt="Demo Graph Right to Left" />

## Documentation

In order to create the directory graphs call the `main` function in `graph_dir.py`:

```python
main(directory_name, orientation=orientation, data=data, show_files=show_files)
```

### Arguments

Argument | Default | Description
--- | --- | ---
`directory_name` | N/A | The name of the directory you'd like to create a graph for.
`orientation` | `'LR'` | The orientation of the graph.
`data` | `False` | If `True`, show number of sub-directories and files in each folder, as well as the memory use of each directory and file. If `False` display none of this information.
`show_files` | `True` | If `True` show all files in each directory. If `False`, show no files. 

## GraphViz Note

In order for the visual representation with Graphviz to work, Graphviz must be downloaded. Download GraphViz here: https://graphviz.gitlab.io/download/. Once downloaded go to `graph_dir.py` and change the System Path under `GRAPHVIZ PATH SETUP`. Replace `'C:\\Graphviz\\bin'` with the path to the bin folder of the downloaded GraphViz folder.

```python
# Change PATH setup for Graphviz directory here:
# --------------------------GRAPHVIZ PATH SETUP------------------------- #
os.environ['PATH'] += os.pathsep + 'C:\\Graphviz\\bin' # <-- Replace this
# ---------------------------------------------------------------------- #
```