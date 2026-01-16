#!/bin/python3
import argparse

import irsl_choreonoid.cnoid_util as iu

from generate_utils import get_jointnamelist

if __name__=='__main__':
    parser = argparse.ArgumentParser(
            prog='generate_jointlist.py', # プログラム名
            usage='', # プログラムの利用方法
            add_help=True, # -h/–help オプションの追加
            )
    parser.add_argument('--bodyfile', type=str, default="robotname.body")
    
    args = parser.parse_args()
    fname = args.bodyfile

    rbody = iu.loadRobot(fname)
    jointnames = get_jointnamelist(rbody)
    for jointname in jointnames:
        print('- "{}"'.format(jointname))
