# Script Documentation
The `main.py` file contains the code that is necessary
to plot the content of both the `histogram` folder and 
the `time_evolution` folder. 

The `csi.csv` file contains the data to be plotted: as 
indicated by the filename extension, it contains 
comma-separated values (strings), each of them representing 
a complex number (that is formatted as needed within 
`main.py` in order to have the numbers parsed correctly 
by Python).
Essentially, the `csi.csv` file contains an _n * 256_ table, 
where 256 is the number of studied sub-carriers, and _n_ 
is the number of packets sampled on each sub-carrier. 
It is important to know the number of sampled packets 
(column length) because 
the `main.py` file contains a function that needs a divisor 
of the column length as a default parameter to split every 
column in equally-long batches. 
This divisor must be manually modified in the script and 
can be found among the parameters of the
`plot_histogram_for_sc` function.

The `unnecessaryPlots` file contains the names of the 
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
(except for `main.py`) stay unaltered 
because they are embedded as strings in the code, 
therefore their change would cause the script not to compile
and run correctly. 