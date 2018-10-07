# INPUT FILES FOR SNANA simulations of PLAsTiCC.

These are input files used on midway to produce PLAsTiCC simulations for the WFD and DDF fields for 10 years for a cadence specified through a simlib. The contents, usage and evolution of these files is explained below.

## CONTENTS
A set of files in the [example_data directory](./gen_plasticc/example_data) and include the directory `PLASTICC_SIMGEN_TEMPLATE`.


## Usage in SNANA
To use these files, a user should change the GENVERSION on the `SIMGEN_MASTER_LSST_DDF_Y10.INPUT` and `SIMGEN_MASTER_LSST_WFD_Y10.INPUT`. The minimal change required is to change `USERNAME_` to a name that identifies a user.  

To run the simulations on midway : run 
```
nohup sim_SNmix.pl SIMGEN_MASTER_LSST_WFD_Y10.INPUT > ${USER}_WFD.log 2>&1 & 
nohup sim_SNmix.pl SIMGEN_MASTER_LSST_DDF_Y10.INPUT > ${USER}_WFD.log 2>&1 & 
```

## PROVENANCE
These files are being maintained from the SRD simulations by Renee Hlozek and Dan Scolnic, and the explanations collected in their document `README_BaselineSimulation`. For evolution of these files, please see [CHANGELOG.md](./CHANGELOG.md)

## Using the build scripts
The build scripts should work on python 2.7 and python 3.6+. If you would like to install python 3.6 and don't have it you can use:
```
bash install/install_python.sh
```
- Install the package using 
```
bash install install/install_all.sh
```
## Getting Started in creating build scripts

- Install the code:
```
python setup.py develop
```
put code you need as part of the package in `build_snana_inputs` and add approriately to the `__init__` module. The preferred way is to add an `__all__` to the module file, listing the classes to be imported. and then haveing a ```from .filename import * ``` in the `__init__.py` file.
- The directory of data files (templates for SNANA) can be obtained after importing the package at 
`build_snana_input.data`
- scripts using these should be in a `scripts` directory.
- Please remember to change the version file `build_snana_input/version.py` by incrementing the version number  
