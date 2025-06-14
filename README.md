# QEST-FORMATS 2025 iCORE Application Data/Scripts
This repository contains scripts to fetch data (mostly from Scopus), as well
as some of the fetched data (June 2025).

For the scripts, you may need to install some packages (see `requirements.txt`)
or have access to the Scopus website and API (this holds for `h_index.py` in
particular).

## Recovering main graphs
* Use `comp.py` with either A or B to obtain the plots for citation counts.
* The `avg.py` script is a copy of the one above where the first plot is given
  in terms of percentages instead of absolute paper numbers.
* Use `acc.py` to plot graphs about the acceptance rates of the conferences.
