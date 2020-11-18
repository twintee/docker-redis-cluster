#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from os.path import join, dirname, abspath, isfile, isdir
import shutil
import argparse

dir_scr = dirname(abspath(__file__))
sys.path.append(join(dir_scr, ".."))
import helper as fn

dir_scr = dirname(abspath(__file__))

def main(_args):
    print("----- redis env setting start.")
    env_file = join(dir_scr, '.env')
    env_org = join(dir_scr, "_org", '.env')
    if not isfile(env_file):
        shutil.copyfile(env_org, env_file)
    params = fn.getenv(env_file)
    if _args.node == 'master':
        if params['MASTER_PASS'] == "":
            params['MASTER_PASS'] = fn.randstr(30)
        req_keys = [
            'TZ',
            'MASTER_PORT',
            'MASTER_PASS',
            'MEM',
        ]
        fn.setparams(params, req_keys)
        if params['SLAVE_PASS'] == "":
            params['SLAVE_PASS'] = params['MASTER_PASS']
        if params['SLAVE_PORT'] == params['MASTER_PORT']:
            params['SLAVE_PORT'] = str(int(params['MASTER_PORT'])+1)
        params['MASTER_HOST'] = fn.local_ip()
    elif _args.node == 'slave':
        if params['SLAVE_PASS'] == "":
            params['SLAVE_PASS'] = fn.randstr(30)
        req_keys = [
            'TZ',
            'SLAVE_PORT',
            'SLAVE_PASS',
            'MASTER_HOST',
            'MASTER_PORT',
            'MASTER_PASS',
            'MEM',
        ]
        fn.setparams(params, req_keys)
        params['SLAVE_HOST'] = fn.local_ip()

    params['NODE'] = _args.node
    fn.setenv(params, env_file)

    for k,v in params.items():
        print(f"{k}={v}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='set env params')
    parser.add_argument('node', help="require node type 'master' or 'slave'")
    args = parser.parse_args()
    if not args.node in ["master", "slave"]:
        print("[error] args error.")
        sys.exit()
    main(args)
