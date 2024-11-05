# Script Documentation

The input data must be structured as follows:

* main folder indicating the bandwidth and modulation scheme
  (e.g. 40ax)
* one sub-folder for each experiment performed using the
  specified bandwidth and modulation scheme
* one `csv` file for each experiment containing the data to process

Example:

```
working directory
├── main.py
├── ...
├── 40ax
│   ├── capture0
│   │   ├── 2020-06-02_15-00-00.csv
│   │   ├── 2020-06-02_15-00-01.csv
│   │   ├── ...
│   ├── capture1
│   │   ├── 2020-06-02_15-00-00.csv
│   │   ├── 2020-06-02_15-00-01.csv
│   │   ├── ...
├── 80ac
│   ├── capture0
│   │   ├── 2020-06-02_15-00-00.csv
│   │   ├── 2020-06-02_15-00-01.csv
│   │   ├── ...
│   ├── capture1
│   │   ├── 2020-06-02_15-00-00.csv
│   │   ├── 2020-06-02_15-00-01.csv
│   │   ├── ...
```

This structure allows for the code to automatically process the input
CSIs and keep the correct data structures to support the implemented
analyses. The code is designed to be easily adaptable to different
input data structures, as long as the input folders are structured in
a consistent way.

Every `csv` file contains the data to manipulate: as
indicated by the filename extension, they contain
comma-separated values (strings), each of them representing
a complex number (that is formatted as needed within the code
in order to have the numbers parsed correctly
by Python).
Essentially, they contain an _n * m_ table,
where _m_ is the number of studied sub-carriers, and _n_
is the number of packets sampled on each sub-carrier.
The setup of the _m_ parameter is automatic and depends on
the channel bandwidth and modulation scheme (e.g. ac, ax).

The [dontPlot](dontPlot) folder contains one file for each
combination of bandwidth and modulation scheme.
Each file lists the names of the
sub-carriers that do not need to be processed because they
are suppressed in transmission, therefore are not currently
relevant to the purpose of this study.
If necessary, it is possible to add other sub-carriers to
the lists contained in these files.

## Libraries

The required libraries are specified in [requirements.txt](requirements.txt)
, alongside their versions.

## Notes

The code is not optimized for speed or memory usage yet.

## Related work

This code is part of the work done for the Master's thesis by
Elena Tonini, titled "Statistical Analysis to Support CSI-Based Sensing Methods".

The thesis is available at the following
[link](https://ans.unibs.it/assets/documents/thesis/tesiMS_elena_tonini.pdf).

If you want to cite the thesis, please use the following BibTeX entry:

```bibtex
@mastersthesis{msctonini2024,
    author  = {Tonini, Elena},
    title      = {{Statistical Analysis to Support CSI-Based Sensing Methods}},
    school  = {{University of Brescia, Department of Information Engineering --- Advanced Networking Systems (ANS) group}},
    year    = {2024},
    month = {9}
}
```