from CDP.Domains import DOMStorage, Log, Network, Runtime


def CDP_initialize():
    DOMStorage.disable()
    Log.disable()
    Network.setCacheDisabled(True)
    Runtime.discardConsoleEntries()
