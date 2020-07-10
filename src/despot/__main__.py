from importlib import import_module
from base64 import urlsafe_b64encode
from os import urandom
from pathlib import Path

from .classes import Despot
from .util.reg import _DespotRegistry

def main():
    dpt = Despot()
    hooks = dpt.config.get('hooks', [])
    for p in map(Path, hooks):
        # Run each hook
        rand_modname = urlsafe_b64encode(urandom(12))
        rand_modname = rand_modname.decode('utf-8')
        loader = SourceFileLoader(rand_modname, str(p.absolute()))
        loader.load_module(rand_modname)
    
    who = dpt.config.get('who', 'Despot')
    if who != 'Despot':
        dpt = _DespotRegistry()
    
    dpt.run()
        
if __name__ == '__main__':
    SystemExit(main())