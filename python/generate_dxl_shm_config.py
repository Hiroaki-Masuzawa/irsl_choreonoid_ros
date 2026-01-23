#!/bin/python3
import argparse

import irsl_choreonoid.cnoid_util as iu

from generate_utils import get_jointnamelist


if __name__=='__main__':
    parser = argparse.ArgumentParser(
            prog='generate_irsl_shm_config.py', # プログラム名
            usage='', # プログラムの利用方法
            add_help=True, # -h/–help オプションの追加
            )
    parser.add_argument('--bodyfile', type=str, default="robotname.body")
    
    args = parser.parse_args()
    fname = args.bodyfile
    rbody = iu.loadRobot(fname)

    num_joint = rbody.getNumJoints()
    jointnames = get_jointnamelist(rbody)

    print("# This file is configlation for irsl_dynamixel_hardware_shm")
    print("")
    print("_default_joint: &default_joint")
    print("  DynamixelSettings:")
    print("    { Return_Delay_Time: 0, Operating_Mode: 3 }")
    print("dynamixel_hardware_shm:")
    print("  port_name: /dev/ttyUSB0")
    print("  baud_rate: 1000000")
    
    print("  joint:")
    for jointname in jointnames:
        print("    #{}:".format(jointname))
        print("    - { ID: XX, <<: *default_joint}")
        
