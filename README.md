# Script Documentation
The `main.py` file contains the code that, by
calling functions contained in other Python files 
whose content is described in section
[Python files content](README.md#python-files-content), 
plots the content of the [histogram](histograms) folder, 
the [time_evolution](time_evolution) folder, and the
[increments_hist](increments_hist) folder. 

The [csi.csv](csi.csv) file contains the data to be plotted: as 
indicated by the filename extension, it contains 
comma-separated values (strings), each of them representing 
a complex number (that is formatted as needed within the code
in order to have the numbers parsed correctly 
by Python).
Essentially, the `csi.csv` file contains an _n * 256_ table, 
where 256 is the number of studied sub-carriers, and _n_ 
is the number of packets sampled on each sub-carrier. 
It is important to know the number of sampled packets 
(column length) because 
the `histograms_plotter.py` file contains a function that 
needs a divisor 
of the column length as a default parameter to split every 
column in equally-long batches. 
This divisor must be manually modified in the script and 
can be found among the parameters of the
`plot_histogram_for_sc` function in `histograms_plotter.py`.

The [unnecessaryPlots](unnecessaryPlots) file contains the names of the 
sub-carriers that do not need to be plotted because they 
are unused for modulation, therefore are not currently 
relevant to the purpose of this study.
If necessary, it is possible to add other sub-carriers to
the list contained in this file. In order to do so, one 
can simply add to the file a new line containing the 
string "SC" followed
by the number of the sub-carrier that does not need to be
plotted. 

It is fundamental that the names of all files and folders
(except for those having a `.py` extension) stay unaltered 
because they are embedded as strings in the code, 
therefore their change would cause the script not to compile
and run correctly. 

## Python files content
Below are listed the Python files whose methods are called
in [main.py](main.py): 
* [histograms_plotter.py](histograms_plotter.py): contains functions that are used
to plot a magnitude/relative frequency histogram 
for each sub-carrier, including functions used to verify 
whether a process is stationary, divide the column 
corresponding to a process in batches, and process each batch
* [increments_plotter.py](increments_plotter.py): contains functions that are used
to plot an increment/frequency histogram 
for each sub-carrier
* [time_evolution_plotter.py](time_evolution_plotter.py): contains a function that is used
to plot a graph representing the evolution of the signal
magnitude over time for each sub-carrier