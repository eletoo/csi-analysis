# Script Documentation

Every `csv` file contains the data to manipulate: as
indicated by the filename extension, they contain
comma-separated values (strings), each of them representing
a complex number (that is formatted as needed within the code
in order to have the numbers parsed correctly
by Python).
Essentially, they contain an _m * n_ table,
where _m_ is the number of studied sub-carriers, and _n_
is the number of packets sampled on each sub-carrier.
The setup of the _m_ parameter is automatic and depends on the value
of the bandwidth of the studied channel set up by the user in
[main.py](main.py) (see Section [Main Script](README.md#Main Script)).

The [unnecessaryPlots](unnecessaryPlots80ax) file contains the names of the
sub-carriers that do not need to be plotted because they
are unused for modulation, therefore are not currently
relevant to the purpose of this study.
If necessary, it is possible to add other sub-carriers to
the list contained in this file. To do so, one
can simply add to the file a new line containing the
string "SC" followed
by the number of the sub-carrier that does not need to be
plotted.

It is fundamental that the names of all files and folders
(except for those having a `.py` extension) stay unaltered
because they are embedded as strings in the code,
therefore their change would cause the script not to compile
and run correctly.

## Main Script

The [main.py](main.py) file contains the code that, by
calling functions contained in other Python files -
whose content is described in section
[Python files content](README.md#python-files-content) -
plots the content of the folders named after the specified
`csi` file.

Every folder contains the following multiple sub-folders:

* [artificial_increments](artificial_increments):
  contains the outputs of the manipulation of artificially generated
  data. The code generating the content of this folder is contained
  in the [artificial_trace_processor.py](artificial_trace_processor.py) file.

* [auto-correlation_graphs](auto-correlation_graphs):
  auto-correlation graphs plotted using python's
  `statsmodels.graphics.tsaplots.plot_acf` function in
  [autocorrelation_plotter.py](autocorrelation_plotter.py)

* [auto-correlation_through_formulae](auto-correlation_through_formulae):
  auto-correlation graphs plotted using manually-typed formulae in
  [autocorrelation_plotter.py](autocorrelation_plotter.py)

* [best_fits_params](best_fits_params) and sub-folders: each sub-folder
  is named after one of the five distributions that best fit the increments
  of the sub-carriers. Each folder contains the plots of the values of
  the parameters that characterize the distribution naming the folder.
  The plot is done through the code in [best_fits_param_calculator.py](best_fits_param_calculator.py)

* [fit_by_sc](fit_by_sc): files containing the values of sum of square
  errors, Akaike and Bayesian Information Criterion for each of the
  listed distributions, which are the five best-fitting distributions
  for the selected sub-carrier. The distributions are selected among
  a list of the ten most common. The code generating this folder
  is in [fitting_by_sc.py](fitting_by_sc.py)

* [fit_by_sc_2](fit_by_sc_2): files containing the values of sum of square
  errors, Akaike and Bayesian Information Criterion for each of the
  listed distributions, which are the five best-fitting distributions
  for the selected sub-carrier. The distributions are selected based
  on a list specified by the user in [main.py](main.py). The code
  generating this folder is in [fitting_by_sc.py](fitting_by_sc.py)

* [fit_increments](fit_increments) and sub-folders: files containing the values of sum of square
  errors, Akaike and Bayesian Information Criterion for each of the
  listed distributions, which are the five best-fitting distributions
  for the increments of the selected sub-carrier.
  The distributions are selected based
  on a list specified by the user in [main.py](main.py). The code
  generating this folder is in [fitting_by_sc.py](fitting_by_sc.py)

* [fit_specific_dists](fit_specific_dists): files containing the
  output of the fitting of the increments of specific distributions.

* [histograms](histograms): histograms of the sub-carriers plotted
  by [histograms_plotter.py](histograms_plotter.py)

* [increments_hist](increments_hist): histograms of the increments
  of each sub-carrier plotted by [increments_plotter.py](increments_plotter.py)

* [merged_plot](merged_plot): plots and information about merged data
  and merged increments generated by [merged_plotter.py](merged_plotter.py)

* [params](params): standard deviation, kurtosis and skewness for
  data and increments generated by [parameters_calculator.py](parameters_calculator.py)

* [time_evolution](time_evolution): plots of the evolution of the
  amplitude of the packets through time for each sub-carrier generated
  by [time_evolution_plotter.py](time_evolution_plotter.py)

## Python files content

Below are listed the Python files whose methods are called
in [main.py](main.py):

* [artificial_trace_processor.py](artificial_trace_processor.py):
  generates and processes artificial traces
* [auto-correlation_plotter.py](autocorrelation_plotter.py):
  contains functions that are used to plot graphs representing
  the auto-correlation process for each sub-carrier
* [best_fits_param_calculator.py](best_fits_param_calculator.py):
  contains functions that are used to fit the five distributions
  that best fit the merged increments onto each sub-carrier
  and to calculate and plot their parameters
* [fitting_by_sc.py](fitting_by_sc.py): contains functions that
  are used to find the best-fitting distribution for each
  sub-carrier and for the distributions of the increments
  of each sub-carrier and save each output in a dedicated file
* [histograms_plotter.py](histograms_plotter.py): contains functions that are used
  to plot a magnitude/relative frequency histogram
  for each sub-carrier, including functions used to verify
  whether a process is stationary, divide the column
  corresponding to a process in batches, and process each batch
* [increments_plotter.py](increments_plotter.py): contains functions that are used
  to plot an increment/frequency histogram
  for each sub-carrier
* [merged_plotter.py](merged_plotter.py): contains the functions
  that are used to elaborate the merged increments (i.e. by
  considering all the increments as if they belonged to a single
  sub-carrier)
* [parameters_calculator.py](parameters_calculator.py): contains
  the functions that are used to calculate variance, skewness
  kurtosis for each sub-carrier and for the distribution of
  the increments of each sub-carrier
* [std_deviation_and_kurtosis_plotter.py](std_deviation_and_kurtosis_plotter.py):
  contains a function used to plot standard deviation and kurtosis
  calculated on the increments of each sub-carrier
* [time_evolution_plotter.py](time_evolution_plotter.py): contains a function that is used
  to plot a graph representing the evolution of the signal
  magnitude over time for each sub-carrier

## Libraries

The code is written in Python 3.6.5 and uses the following libraries:

* [numpy](https://www.numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [matplotlib](https://matplotlib.org/)
* [scipy](https://www.scipy.org/)
* [statsmodels](https://www.statsmodels.org/stable/index.html)
* [fitter](https://github.com/cokelaer/fitter)

The required versions are specified in [requirements.txt](requirements.txt).

## How to run the code

The code can be run by executing [main.py](main.py) using Python 3.6.5.

## Notes

The code is not optimized for speed yet.
It is intended to be used as the source code to plot the data and graphs
described in the previous sections.

The folders whose contents have been used in the thesis titled
''Analysis and Characterization of Wi-Fi Channel State Information''
by Elena Tonini are:

* [csi](csi)
* [training2_192_168_2_4](training2_192_168_2_4)
* [training2_192_168_2_10](training2_192_168_2_10)