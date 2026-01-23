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
    parser.add_argument('--joint_controller_name', type=str, default="trajectory_controller")
    
    args = parser.parse_args()
    fname = args.bodyfile
    rbody = iu.loadRobot(fname)

    jointnames = get_jointnamelist(rbody)
    print("joint_state_controller:")
    print("  type: joint_state_controller/JointStateController")
    print("  publish_rate: 50")
    print("  joints:")
    for jointname in jointnames:
        print('    - "{}"'.format(jointname))
    print("{}:".format(args.joint_controller_name))
    print("  type: position_controllers/JointTrajectoryController")
    print("  joints:")
    for jointname in jointnames:
        print('    - "{}"'.format(jointname))
