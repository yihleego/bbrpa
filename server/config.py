# -*- coding=utf-8
import os
from dataclasses import dataclass

import yaml

from constants import ROOT_DIR, ENV


@dataclass
class Logging:
    level: str
    format: str
    filename: str


@dataclass
class Database:
    url: str

@dataclass
class Redis:
    host: str
    port: int
    password: str


with open(os.path.join(ROOT_DIR, f"config-{ENV}.yml"), "r", encoding="utf-8") as f:
    _config = yaml.safe_load(f)

# exports
logging = Logging(**_config.get("logging"))
database = Database(**_config.get("database"))
redis = Redis(**_config.get("redis"))
