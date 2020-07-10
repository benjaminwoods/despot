#radon integration

from radon.cli import Config, FileConfig
from radon.cli.harvest import CCHarvester

import radon.complexity as cc_mod

_cfg = FileConfig()

def ccjson(paths):
    """
    Modified version of radon.cli.cc.
    
    This silently returns the digest as a JSON (string).
    """
    
    config = Config(
        min=_cfg.get_value('cc_min', str, 'A').upper(),
        max=_cfg.get_value('cc_max', str, 'F').upper(),
        exclude=_cfg.get_value('exclude', str, None),
        ignore=_cfg.get_value('ignore', str, None),
        show_complexity=_cfg.get_value('show_complexity', bool, False),
        average=_cfg.get_value('average', bool, False),
        total_average=_cfg.get_value('total_average', bool, False),
        order=getattr(cc_mod,
                      _cfg.get_value('order', str, 'SCORE').upper(),
                      getattr(cc_mod, 'SCORE')),
        no_assert=_cfg.get_value('no_assert', bool, False),
        show_closures=_cfg.get_value('show_closures', bool, False),
        include_ipynb=_cfg.get_value('include_ipynb', bool, False),
        ipynb_cells=_cfg.get_value('ipynb_cells', bool, False)
    )
    
    harvester = CCHarvester(paths, config)
    
    return harvester.as_json()