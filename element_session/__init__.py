from datajoint import config

if "custom" not in config:
    config["custom"] = {}

DB_PREFIX = config["custom"].get("database.prefix", "datajoint-element_")
