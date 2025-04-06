# vsauto

`vsauto` uses [pluggy](https://github.com/pytest-dev/pluggy) to provide potentially convenient loading of [vapoursynth](https://github.com/vapoursynth/vapoursynth) plugins distributed as part of python packages.

## Basic usage

If you are writing a script and simply wish to load installed plugins you can do so trivially.

```py
import vsauto

vsauto.load()
# All installed plugins are now loaded
```

Note that due to the way pluggy works, any plugin throwing an exception while loading will stop loading and this cannot be gracefully handled to continue loading other plugins. For this reason it is recommend that if you are writing a package and want to load your package's dependencies that you limit what you attempt to load.

```py
import vsauto

# Note these are the python package names that will be loaded.
# These could load any vapoursynth plugin(s).

vsauto.load("example-a") # Loads only "example-a"
vsauto.load(["example-b", "example-c"]) # Loads both "example-b" and "example-c"
# Only example-a, example-b, and example-c have been loaded

vsauto.load("example-a") # Does nothing since "example-a" was already loaded, but is harmless
```

## Motivation

This project aims to improve the ergonomics of using vapoursynth plugins and python packages together.

There's a lot of python code that can help wrap and combine vapoursynth plugins to provide a more powerful and convenient interface for developers (see for example [vs-jeptack](https://github.com/Jaded-Encoding-Thaumaturgy/vs-jetpack)). But the distribution of vapoursynth plugins and python packages has historically been completely separate. With end users mostly using `pip` to install python packages and `vsrepo` (or manual installation) for vapoursynth plugins, but `pip` isn't aware of dependencies on `vsrepo` and vice versa.

By offering a convenient means of loading vapoursynth plugins from python packages it becomes possible to express these dependencies (and even version requirements) in a way that `pip` can understand, and is thus easy for end users with a single tool.

## Distributing a vapoursynth plugin

If you have a vapoursynth plugin you want to distribute as part of a python package there are only a few requirements imposed by this project.

First you must register a [setuptools entry point](https://setuptools.pypa.io/en/latest/userguide/entry_point.html) where the entrypoint name matches the package name.

```toml
[project]
name = "example"

[project.entry-points.vsauto]
example = "example"
```

Then your project must expose the appropriate [hookimpl](https://pluggy.readthedocs.io/en/stable/#implementations).

```py
import vsauto

namespace = "example"

@vsauto.hookimpl
def loadPlugin():
    import logging
    import platform
    import importlib
    import vapoursynth as vs

    from pathlib import Path

    # Gracefully handling cases where vapoursynth has autoloaded a plugin
    # with the same namespace is strongly encouraged.
    preloaded = next((plugin for plugin in vs.core.plugins() if plugin.namespace == namespace), None)
    if preloaded:
        logger.warning(f"A plugin at '{Path(preloaded.plugin_path)}' has prevented loading '{__name__}'. Please remove the conflicting package or auto-loaded plugin if you wish to use this version.")
        return

    if platform.system() == "Windows":
        vs.core.std.LoadPlugin(importlib.resources.files(__name__) / "data" / "windows" / f"lib{namespace}.dll")
    else:
        logger.warning(f"No binary pypi distribution of '{__name__}' exists for your platform.")
```

Bundling the library into the python package is left as an excercise for the reader. Tools like [Flit](https://flit.pypa.io/en/stable/) make it straightforward to include binary resources in wheel, but I have not found a straightforward way to create per-OS+arch wheels with only the relevant binary resouces included. Please share any working examples if you have suggestions.