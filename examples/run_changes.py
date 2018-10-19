import os
from argparse import ArgumentParser
from  gen_plasticc import copy_template_to, execute_bashscript



# Modify MAKE_SIMGEN_MASTER
# Change CIDRAN_MIN_WFD=1000000
# to 0

# Run MAKE_SIMGEN_MASTER


if __name__ == '__main__':

    parser = ArgumentParser(description='Generate inputs for PLASTICC sims')
    parser.add_argument('--pathtodir', type=str,
                        help='absolute path to directory where we want to have plasticc inputs', 
                        default='./plasticc_sims_test') 


    args = parser.parse_args()
    loc = args.pathtodir
    opsimname = 'kraken_2026'
    simlib_path = '/Users/rbiswas/data/LSST/OpSimData/kraken_2026_WFD.simlib.COADD'

    # copy the template to pathdir
    copy_template_to(loc)

    # Modify `SIMGEN_TEMPLATE_LSST.INPUT`  : CURRENT NEED : IGNORE (read below for detailed explanation)
    ## What needs to be changed: (the range of peakmjd needs to match the simlib range
    ## Note this is different between minion and later versions for example.
    ## The latest versions of opsim are all the same, so changing CWP simlibs, we don't have to do anything
    ## Keys to change : 
    ### GENRANGE_MJD:      59842 63502   # full 10 years
    ### GENRANGE_PEAKMJD:  59782 63577   # PEAKMJD cut is wider to catch rise time, making -60, + 75 from prev
    ### Proposed solution : Change SIMGEN_TEMPLATE_LSST_INPUT to values suitable for CWP
    ### Add method to handle such changes automatically  later. 


    # Modify `SIMGEN_MASTER_XXX.INPUT` : CURRENT NEED (some of these changes) 
    
    ## RESET_CID flag: CURRENT NEED : IGNORE 
        ## Issue:
        ## RESET_CID: 2 is a line needed to get unique CIDs for each object
        ## Currently working without these, so CID unique within models, removed this line
        ## NEED TO ADD back if we generate plasticc

    # Change all _XXXOPSIM_MODEL to _ALT_SCHED_OPSIM_MODEL or appropriate simlib name
    template_file = os.path.join(loc, 'SIMGEN_MASTER_XXX.INPUT.TEMPLATE')
    out_file = os.path.join(loc, 'SIMGEN_MASTER_XXX.INPUT')
    with open(template_file, 'r') as f:
        data = f.read()
        data.replace('XXXOPSIM', opsimname)
        data.replace('SIMLIB_PATH', simlib_path)
    with open(out_file, 'w') as g:
        g.writelines(data)

    # Run Rick's bash script 
    bash_script = './MAKE_SIMGEN_MASTER'
    execute_bashscript(bash_script, loc=loc)


    # Change the solid angle in the WFD and DDF inputs (alternatively, we could have changed them in the bash script)
    # change GENOPT_GLOBAL: SIMLIB_FILE $LSST_ROOT/simlibs/minionv4_1016_XXXSURVEY.simlib.COADD SOLID_ANGLE XXXSOLIDANGLE  SEARCHEFF_zHOST_FILE $PLASTICC_ROOT/SIMGEN/SEARCHEFF_zHOST_PLASTICC_XXXSURVEY.DAT
    # fname = os.path.join(dirname, 'SIMGEN_MASTER_XXX.INPUT') 
