from pluggy import PluginManager
from pluggy._manager import DistFacade

# Allows specifying multiple names and only loads if entrypoint name matches package name
class StrictPluginManager(PluginManager):
    def strict_load_setuptools_entrypoints(self, group, names=None):
        """Load modules from querying the specified setuptools ``group``.

        :param group:
            Entry point group to load plugins.
        :param names:
            If given, loads only plugins with the given ``names``.

        :return:
            The number of plugins loaded by this call.
        """
        import importlib.metadata

        # Iterating over strings is probably unexpected in this context
        if isinstance(names, str):
            names = (names,)
        
        count = 0
        for dist in list(importlib.metadata.distributions()):
            for ep in dist.entry_points:
                if (
                    ep.group != group
                    or ep.name != dist.name
                    or (names is not None and ep.name not in names)
                    # already registered
                    or self.get_plugin(ep.name)
                    or self.is_blocked(ep.name)
                ):
                    continue
                plugin = ep.load()
                self.register(plugin, name=ep.name)
                self._plugin_distinfo.append((plugin, DistFacade(dist)))
                count += 1
        return count