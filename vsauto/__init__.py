"""Allow dynamically loading vapoursynth plugins via pluggy"""

__version__ = "0.0.1"

import pluggy

from . import hookspecs
from .lib import StrictPluginManager

hookimpl = pluggy.HookimplMarker("vsauto")

manager = StrictPluginManager("vsauto")
manager.add_hookspecs(hookspecs)
manager.hook.loadPlugin.call_historic()

def load(names=None):
    import logging
    logger = logging.getLogger(__name__)
    num_loaded = manager.strict_load_setuptools_entrypoints("vsauto", names)
    logger.debug(f"Loaded {num_loaded} plugins.")
