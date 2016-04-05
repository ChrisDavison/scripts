# pyscripts
All my useful python scripts and snippets that don't quite deserve their own full module

I already have `cdutils` and `cddata`, but I may remove these, as it is a bit of a nuisance 
to have to restart running iPython notebook instances, and much of this code will be updated
over time, and added to.

As these scripts grow, I may deem it necessary to export functionality back into separate
modules, but for now, this is good enough.

## Functionality

### Root
- `convert_units` with a sensitivity and precision, give ADC values actual units
- `hmm_params` to read in HMM parameters from a file
- `log` to set up a logger to append to a file
- `os` to create directories based on date, and filter files
- `plot` to prettify matplotlib axes
- `time` to fix buggy timestamps

### Data
- `handling` to return subsets of data from pandas dataframes
- `info` to get info about pandas dataframes

### DSP
- `calculus` for integral and derivative of a signal
- `fft` to perform the fft of a signal
- `filter` to do lowpass, highpass and bandpass filtering
