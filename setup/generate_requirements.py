import os

requirement_files = ['install/pip-requirements.txt',
                     'install/conda_requirements_anaconda.txt',
                     'install/conda_requirements_conda_forge.txt']
lines = []

for fname in requirement_files:
    if os.path.exists(fname):
        with open('install/pip-requirements.txt', 'r') as f:
            lines = f.read() 
res = (list('- ' + l  +'\n' for l in lines.split('\n')))
with open ('install/requirements.md', 'wb') as f:
    f.write('# Required Packages beyond miniconda install\n'.encode())
    for l in res[:-1]:
        f.write(l.encode())
