from initialize import driver


"""
Documentation:
    https://chromedevtools.github.io/devtools-protocol/
"""

class DOMStorage:

    def clear(storageId: dict) -> dict:
        """
        storageId Properties:
            securityOrigin    - Optional  :  Security origin for the storage. (str) 
            storageKey        - Optional  :  Represents a key by which DOM Storage keys its CachedStorageAreas. (str)
            isLocalStorage    - Required  :  Whether the storage is local storage (not session storage). (bool)
        """
        params = {
            "storageId": storageId
        }
        obj: dict = driver.execute_cdp_cmd("DOMStorage.clear", params)
        return obj

    def disable() -> dict:
        obj: dict = driver.execute_cdp_cmd("DOMStorage.disable", {})
        return obj

    def getDOMStorageItems(storageId: dict) -> list:
        params = {
            "storageId": storageId
        }
        obj: dict = driver.execute_cdp_cmd("DOMStorage.getDOMStorageItems", params)
        return obj


class Log:

    def disable() -> dict:
        obj: dict = driver.execute_cdp_cmd("Log.disable", {})
        return obj


class Network:

    def clearBrowserCache() -> dict:
        obj: dict = driver.execute_cdp_cmd("Network.clearBrowserCache", {})
        return obj

    def disable() -> dict:
        obj: dict = driver.execute_cdp_cmd("Network.disable", {})
        return obj

    def setCacheDisabled(cacheDisabled: bool) -> dict:
        params = {
            "cacheDisabled": cacheDisabled
        }
        obj: dict = driver.execute_cdp_cmd("Network.setCacheDisabled", params)
        return obj

    # DEPRECATED
    def canClearBrowserCache() -> bool:
        obj: dict = driver.execute_cdp_cmd("Network.canClearBrowserCache", {})
        return obj["result"]

    def setBlockedURLs(urls: list) -> dict:
        params = {
            "urls": urls
        }
        obj: dict = driver.execute_cdp_cmd("Network.setBlockedURLs", params)
        return obj


class Runtime:

    def disable() -> dict:
        obj: dict = driver.execute_cdp_cmd("Runtime.disable", {})
        return obj

    def discardConsoleEntries() -> dict:
        obj: dict = driver.execute_cdp_cmd("Runtime.discardConsoleEntries", {})
        return obj
