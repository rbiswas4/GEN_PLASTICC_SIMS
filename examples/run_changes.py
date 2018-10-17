import os
from  gen_plasticc import copy_template_to

location = '/Users/rbiswas/tmp'
dirname =  'pdir'

copy_template_to(location, dirname)

dirname = os.path.join(location, dirname)

# Modify `SIMGEN_TEMPLATE_LSST.INPUT` if necessary to change 
## What needs to be changed: (the range of peakmjd needs to match the simlib range
## Note this is different between minion and later versions for example.
## The latest versions of opsim are all the same, so changing CWP simlibs, we don't have to do anything
## Keys to change : 
# GENRANGE_MJD:      59842 63502   # full 10 years
# GENRANGE_PEAKMJD:  59782 63577   # PEAKMJD cut is wider to catch rise time, making -60, + 75 from prev
### Proposed solution : Change SIMGEN_TEMPLATE_LSST_INPUT to values suitable for CWP
### Add method to handle such changes automatically  later. 

# Modify `SIMGEN_MASTER_XXX.INPUT`

## Need to change the following key
## If we do this, then we will have CID overlaps between the models,
# RESET_CIDOFF: 2  # flag to generate unique CID for each model
## Proposed solution : 

# Change all _XXXOPSIM_MODEL to _ALT_SCHED_OPSIM_MODEL or appropriate simlib name

# change GENOPT_GLOBAL: SIMLIB_FILE $LSST_ROOT/simlibs/minionv4_1016_XXXSURVEY.simlib.COADD SOLID_ANGLE XXXSOLIDANGLE  SEARCHEFF_zHOST_FILE $PLASTICC_ROOT/SIMGEN/SEARCHEFF_zHOST_PLASTICC_XXXSURVEY.DAT
fname = os.path.join(dirname, 'SIMGEN_MASTER_XXX.INPUT') 
for line in data.split('\n'):
    if line.startswith('RESET_CIDOFF'):
        pass
    for key in changedict.keys():
        if key in line:
            line.replace(

# Modify MAKE_SIMGEN_MASTER
# Change CIDRAN_MIN_WFD=1000000
# to 0

# Run MAKE_SIMGEN_MASTER
