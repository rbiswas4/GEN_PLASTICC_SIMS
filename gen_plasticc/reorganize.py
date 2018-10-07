from __future__ import division, absolute_import, print_function

__all__ = ['copy_template_to']

import os
import shutil
from . import example_data

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

    template_dir : if None, `example_data/PLASTICC_SIMGEN_TEMPLATE`

    """
    dst = os.path.join(location, dirname)

    if create_path:
        raise NotImplementedError('Have not implemented create path yet')


    if template_dir is None:
        template_dir =  os.path.join(example_data, 'PLASTICC_SIMGEN_TEMPLATE')

    shutil.copytree(template_dir, dst)

    return template_dir, dst
