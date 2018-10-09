from __future__ import division, absolute_import, print_function

__all__ = ['copy_template_to']

import os
import shutil
from . import example_data
import subprocess

def execute_bashscript(script):
    """
    Parameters
    ---------
    script : string, mandatory
        absolute path to script to execute
    """
    bash_cmd = 'bash ' + script
    res = subprocess.call(bash_cmd, shell=True)
    return res

def modify_template_file(fname, changes):
    """
    fname: string
        filename in dir
    """
    with open(fname, 'r') as f:
        data = f.read()

    change_string = data
    return changed_string

def copy_template_to(location, dirname, create_path=False, clobber=False,
                     template_dir=None):
    """
    Copies a template directory to a new directory within a given location,
    creating directories if necessary, and clobbering old directories if
    requested.

    Parameters
    ----------
    location : string, mandatory
        location of directory
    dirname :
        name of directory. ie location/directory will be the final path 

    create_path : Not implemented

    clobber : False, 
        Not implemented as true
        if True, and dirname exists as location/dirname, remove the directory
        dirname

    template_dir : if None, `example_data/PLASTICC_SIMGEN_TEMPLATE`

    """
    dst = os.path.join(location, dirname)

    if clobber:
        raise NotImplementedError('Have not implemented clobber yet')
    if create_path:
        raise NotImplementedError('Have not implemented create path yet')


    if template_dir is None:
        template_dir =  os.path.join(example_data, 'PLASTICC_SIMGEN_TEMPLATE')

    shutil.copytree(template_dir, dst)

    return template_dir, dst
