#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os.path import join, dirname, abspath, isfile, isdir
import argparse

from dotenv import load_dotenv

dir_scr = os.path.abspath(os.path.dirname(__file__))
sys.path.append(join(dir_scr, ".."))
import helper as fn

os.chdir(dir_scr)
file_env = os.path.join(dir_scr, ".env")

def main(_args):
    """
    initialize container
    """

    envs = fn.getenv(file_env)
    node = envs['NODE']
    if not _args.node is None:
        node = _args.node
    if node == "":
        print(f"[error] node type not set.")
        sys.exit()

    target = ""
    if node != "all":
        target = f"rds-{node}"

    # サービス削除
    cmd_down = "docker-compose down"
    for line in fn.cmdlines(_cmd=cmd_down):
        sys.stdout.write(line)

    fn.rmdir(join(dir_scr, "vol", node))

    # サービス作成
    for line in fn.cmdlines(_cmd=f"docker-compose up -d {target}"):
        sys.stdout.write(line)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='set env params')
    parser.add_argument('--node', '-n', help="(option) set generate node type. 'master' or 'slave' or 'all'")
    args = parser.parse_args()

    _input = input("initialize container. ok? (y/*) :").lower()
    if not _input in ["y", "yes"]:
        print("[info] initialize canceled.")
        sys.exit()

    print("[info] initialize start.")
    main(args)
    print("[info] initialize end.")
