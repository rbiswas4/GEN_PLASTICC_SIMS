import os
from argparse import ArgumentParser
from  gen_plasticc import copy_template_to, execute_bashscript
import gen_plasticc
import numpy as np



# Modify MAKE_SIMGEN_MASTER
# Change CIDRAN_MIN_WFD=1000000
# to 0

# Run MAKE_SIMGEN_MASTER


if __name__ == '__main__':

    print('using gen_plasticc version', gen_plasticc.__version__)
    parser = ArgumentParser(description='Generate inputs for PLASTICC sims')
    parser.add_argument('--pathtodir', type=str,
                        help='absolute path to directory where we want to have plasticc inputs', 
                        default='./plasticc_sims_test') 
    parser.add_argument('--opsimname', type=str, help='name for OpSim run used in GENVERSION, eg. "kraken_2026"', 
                        default='kraken_2026')
    parser.add_argument('--wfd_simlibpath', type=str, help='absolute path to the wfd simlib', 
                        default='/project/rkessler/SURVEYS/LSST/ROOT/simlibs/cwp/kraken_2026_wfd.simlib.COADD')
    parser.add_argument('--ddf_simlibpath', type=str, help='absolute path to the ddf simlib', 
                        default='/project/rkessler/SURVEYS/LSST/ROOT/simlibs/cwp/kraken_2026_ddf.simlib.COADD')
    parser.add_argument('--no_use_minseason', dest='no_use_minseason', help='if provided any constriant on min_seasons will be skipped', action="store_true", default=False)

    parser.add_argument('--rarifyIaBy', help='a number to decrease abundance of Ia or model 11  by, defaults to 100', default=100, type=float)

    args = parser.parse_args()
    loc = args.pathtodir
    opsimname = args.opsimname
    wfd_simlib_path = args.wfd_simlibpath
    ddf_simlib_path = args.ddf_simlibpath
    skip_minseason_key = args.no_use_minseason

    print('skip_minseason_key', skip_minseason_key)
    rarify_factor = args.rarifyIaBy

    # Check that the simlib paths exist

    # copy the template to pathdir
    copy_template_to(loc)


    # Modify `SIMGEN_INCLUDE_SALT2.INPUT`
    # CURRENT NEED: rarify by a number
    template_file = os.path.join(loc, 'SIMGEN_INCLUDE_SALT2.INPUT')
    with open(template_file, 'r') as f:
        data = f.read()
    data = data.replace('2.5E-5', '{:1.1E}'.format(np.float('2.5E-5')/rarify_factor))
    data = data.replace('9.7E-5', '{:1.1E}'.format(np.float('9.7E-5')/rarify_factor))
    with open(template_file, 'w') as g:
        g.writelines(data)

    # Modify `SIMGEN_TEMPLATE_LSST.INPUT`  : CURRENT NEED : IGNORE (read below for detailed explanation)
    ## What needs to be changed: (the range of peakmjd needs to match the simlib range, and SIMLIB_MKSOPT
    ## Note this is different between minion and later versions for example.
    ## The latest versions of opsim are all the same, so changing CWP simlibs, we don't have to do anything
    ## Keys to change : 
    ### GENRANGE_MJD:      59842 63502   # full 10 years
    ### GENRANGE_PEAKMJD:  59782 63577   # PEAKMJD cut is wider to catch rise time, making -60, + 75 from prev
    ### Proposed solution : Change SIMGEN_TEMPLATE_LSST_INPUT to values suitable for CWP
    ### Add method to handle such changes automatically  later. 
    template_file = os.path.join(loc, 'SIMGEN_TEMPLATE_LSST.INPUT')
    with open(template_file, 'r') as f:
        data = f.read()
    data = data.replace('SIMLIB_MSKOPT:   256  # write every survey observation',
                        'SIMLIB_MSKOPT:   128  # write every observation in seasons overlapping LC')
    with open(template_file, 'w') as g:
        for line in data.split('\n'):
            if skip_minseason_key:
                print('simlib key on')
	        if  'SIMLIB_MINSEASON' in line:
                    print('found line with minseason key')
	        else:
                    g.write(line)
                    g.write('\n')
                 

	    else:
                 g.write(line)
                 g.write('\n')


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
    print(data.count('XXXOPSIM'))
    data = data.replace('XXXOPSIM', opsimname)
    print(data.count('XXXOPSIM'))
    with open(out_file, 'w') as g:
        g.writelines(data)

    # Run Rick's bash script 
    bash_script = './MAKE_SIMGEN_MASTER'
    execute_bashscript(bash_script, loc=loc)


    # Check if WFD file exists and is non-empty
    templatefile = os.path.join(loc, 'SIMGEN_MASTER_LSST_WFD.INPUT')
    assert os.path.exists(templatefile)
    assert os.stat(templatefile).st_size > 0

    # Change the solid angle in the WFD and DDF inputs (alternatively, we could have changed them in the bash script)
    with open(templatefile, 'r') as f:
        data = f.read()
    data = data.replace('SIMLIB_PATH', wfd_simlib_path)
    with open(templatefile, 'w') as f:
        f.writelines(data)

    # Change the solid angle in the WFD and DDF inputs (alternatively, we could have changed them in the bash script)
    templatefile = os.path.join(loc, 'SIMGEN_MASTER_LSST_DDF.INPUT')
    with open(templatefile, 'r') as f:
        data = f.read()
    data = data.replace('SIMLIB_PATH', ddf_simlib_path)
    # data = data.replace('SIMLIB_MSKOPT:   256  # write every survey observation',
    #                    'SIMLIB_MSKOPT:   128  # write every observation in seasons overlapping LC')
    with open(templatefile, 'w') as f:
        f.writelines(data)
