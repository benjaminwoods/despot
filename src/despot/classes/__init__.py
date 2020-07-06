import yaml
from importlib import import_module
from sys import version_info

from ..util import walkmodule, _RulerRegistry

PYTHON_LANG = {'python': version_info}

class Despot:
    def __init__(self, language=PYTHON_LANG):
        self.config = self.__class__.__loadConfig()
        self.rulers = _RulerRegistry()
        self.language = language

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
        cfg = self.config['requirements']['unit']
        if cfg['framework'] == 'pytest':
            self.pytest()
    
    def pytest(self):
        cfg = self.config['requirements']['unit']
        packages = cfg.get('packages', [{}])
        
        for pkg in packages:
            # Output to stdout
            pass
            
            pkgname = pkg.get('name', '.')
            testdir = pkg.get('testdir', '.')
            
            pkg = import_module(pkgname)
            
            for name in walkmodule(pkg):
                self.rulers['nero'](name, testdir, self.language)