# scripts

All my useful scripts (of any language) that don't quite deserve their own repo.

If these scripts get expanded, will perhaps get expanded into their own repos/python modules/binaries
etc as required.

## Functionality

### Root
- `convert_units` with a sensitivity and precision, give ADC values actual units
- `hmm_params` to read in HMM parameters from a file
- `log` to set up a logger to append to a file
- `os` to create directories based on date, and filter files
- `plot` to prettify matplotlib axes
- `time` to fix buggy timestamps
- `passive.sh` to check for passive language usage in prose
- `dups.pl` to find lexical illusions (the the)
- `weasel.sh` to find words that sound good but don't ultimately provide information.

### Data
- `handling` to return subsets of data from pandas dataframes
- `info` to get info about pandas dataframes

### DSP
- `calculus` for integral and derivative of a signal
- `fft` to perform the fft of a signal
- `filter` to do lowpass, highpass and bandpass filtering

## cdutils/cddata

Some of this work was originally split into `cdutils` and `cddata`, but I got sick of restarting
running iPython notebooks (long-term running notebooks) to allow iPython to pick up the newer installed
modules.
