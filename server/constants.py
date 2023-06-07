import os
import argparse


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
