import yaml
from importlib import import_module
from sys import version_info
import re

from ..util.walk import walkmodule
from ..util.reg import _RulerRegistry

PYTHON_LANG = {'python': version_info}

class Despot:
    def __init__(self):
        self.config = self.__class__.__loadConfig()
    
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
        
        for ruler, ruler_cfgs in self.config.get('rulers', {}).items():
            for ruler_cfg in ruler_cfgs:
                language = ruler_cfg.get('lang', PYTHON_LANG)
                packages = ruler_cfg.get('packages', [{}])
                testdir = ruler_cfg.get('testdir', '.')
                ignore = ruler_cfg.get('ignore', [])
                
                (lang, version) = next(iter(language.items()))
                
                if lang == 'python':
                    for pkg in packages:
                        # Output to stdout
                        pass
                        
                        pkgname = pkg.get('name', '.')
                        
                        pkg = import_module(pkgname)
                        
                        for path, name in walkmodule(pkg, find_attr=True):
                            try:
                                for expr in ignore:
                                    if re.match(expr,name):
                                        assert 0
                            except AssertionError:
                                continue
                            
                            self.rulers[ruler](path, name, testdir, language)