# -*- coding=utf-8
import argparse
import os
from dataclasses import dataclass

import yaml


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", default=DEV)
    return parser.parse_args()


def get_env():
    return get_args().env


# constants
ROOT_DIR = os.path.dirname(__file__)
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
BVH_DIR = os.path.join(ROOT_DIR, "config/motion")
MOTION_DIR = os.path.join(ROOT_DIR, "config/motion")
RETARGET_DIR = os.path.join(ROOT_DIR, "config/retarget")
PROD = 'prod'
DEV = 'dev'
TEST = 'test'
DEBUG = 'debug'
# env
ENV = get_env()


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
