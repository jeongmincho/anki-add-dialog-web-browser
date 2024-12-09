from aqt import mw

def get_config():
    return mw.addonManager.getConfig(__name__) or default_config()

def save_config(config):
    mw.addonManager.writeConfig(__name__, config)

def default_config():
    return {
        "start_url": "https://www.google.com"
    }
