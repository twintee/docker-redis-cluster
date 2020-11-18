#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os.path import join, dirname, abspath, isfile, isdir
import time
import shutil

from dotenv import load_dotenv

dir_scr = os.path.abspath(os.path.dirname(__file__))
sys.path.append(join(dir_scr, ".."))
import helper as fn

os.chdir(dir_scr)
file_env = os.path.join(dir_scr, ".env")

def main():
    """
    initialize container
    """

    load_dotenv(file_env)
    node = str(os.getenv("NODE"))
    if node == "":
        print(f"[error] node type not set.")
        sys.exit()

    # コンテナ削除
    cmd_down = "docker-compose down"
    _input = input("initialize volumes. ok? (y/*) :").lower()
    if _input in ["y", "yes"]:
        # ボリューム削除
        print("[info] reset volume.")
        cmd_down = "docker-compose down --volume"
        dir_vol = join(dir_scr, "vol", node)
        os.removedirs(dir_vol)
    for line in fn.cmdlines(_cmd=cmd_down):
        sys.stdout.write(line)
    # コンテナ作成
    for line in fn.cmdlines(_cmd=f"docker-compose up -d rds-{node}"):
        sys.stdout.write(line)

if __name__ == "__main__":

    _input = input("initialize container. ok? (y/*) :").lower()
    if not _input in ["y", "yes"]:
        print("[info] initialize canceled.")
        sys.exit()

    print("[info] initialize start.")
    main()
    print("[info] initialize end.")
