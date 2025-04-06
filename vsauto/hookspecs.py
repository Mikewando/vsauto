import pluggy

hookspec = pluggy.HookspecMarker("vsauto")

@hookspec(historic=True)
def loadPlugin():
    pass