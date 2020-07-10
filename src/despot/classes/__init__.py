import yaml
from importlib import import_module
from sys import version_info

from ..util import walkmodule, _RulerRegistry

PYTHON_LANG = {'python': version_info}

class Despot:
    def __init__(self, language=PYTHON_LANG):
        self.config = self.__class__.__loadConfig()
        self.language = language
    
    @property
    def rulers(self):
        return _RulerRegistry()
    
    @classmethod
    def __loadConfig(cls):
        with open('.despot.yaml') as fp:
            config = yaml.safe_load(fp)

        # Data validation step
        pass

        return config

    def run(self):
        # Data validation step
        pass
        
        if 'unit' in self.config['requirements']:
            # Data validation step
            pass
        
            self.unit()
    
    def unit(self):
        unit_cfg = self.config['requirements']['unit']
        if unit_cfg['framework'] == 'pytest':
            self.pytest()
    
    def pytest(self):
        unit_cfg = self.config['requirements']['unit']
        packages = unit_cfg.get('packages', [{}])
        
        for pkg in packages:
            # Output to stdout
            pass
            
            pkgname = pkg.get('name', '.')
            testdir = pkg.get('testdir', '.')
            
            pkg = import_module(pkgname)
            
            for path, name in walkmodule(pkg):
                self.rulers['nero'](path, name, testdir, self.language)