# IPython log file

import pyyaml
import yaml
d = yaml.load('input.yaml')
d
with open('input.yaml') as f:
    d = yaml.load(f)
    
d
d['WHERE']
get_ipython().run_line_magic('logstart', '')
exit()
