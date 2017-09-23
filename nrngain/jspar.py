import json


def save(pfile, par):
    with open(pfile, 'w') as f:
        json.dump(par, f, sort_keys=True, indent=4)


def load(pfile):
    with open(pfile) as f:
        par = json.load(f)
    return par
