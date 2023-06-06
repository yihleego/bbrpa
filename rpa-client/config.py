# -*- coding=utf-8
import os
from dataclasses import dataclass

import yaml

ROOT_DIR = os.path.dirname(__file__)


@dataclass
class Logging:
    level: str
    format: str
    filename: str


@dataclass
class Server:
    host: str
    port: int
    path: str
    ssl: bool


@dataclass
class App:
    size: int


with open(os.path.join(ROOT_DIR, f"config.yml"), "r", encoding="utf-8") as f:
    _config = yaml.safe_load(f)

# exports
logging = Server(**_config.get("logging"))
server = Server(**_config.get("server"))
app = App(**_config.get("app"))
