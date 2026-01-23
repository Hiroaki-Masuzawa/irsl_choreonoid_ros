#!/bin/python3
import argparse
import numpy
import os
import sys

from distutils.util import strtobool


import irsl_choreonoid.cnoid_util as iu

from generate_utils import get_jointnamelist


if __name__=='__main__':
    parser = argparse.ArgumentParser(
            prog='generate_ri_config.py', # プログラム名
            usage='Demonstration of cnoid_dump_model', # プログラムの利用方法

            add_help=True, # -h/–help オプションの追加
            )
    parser.add_argument('--bodyfile', type=str, default="robotname.body")
    parser.add_argument('--use_wheel', type=strtobool, default=False)
    parser.add_argument('--controller_name', type=str, default="trajectory_controller")
    
    args = parser.parse_args()
    fname = args.bodyfile
    rbody = iu.loadRobot(fname)

    jointnames = get_jointnamelist(rbody)

    num_link = rbody.getNumLinks()
    num_joint = rbody.getNumJoints()
    num_device = rbody.getNumDevices()

    robotname = rbody.getModelName()
    
    print("robot_model:")
    print("  name: {}".format(robotname))
    print("  url: 'file:///{}'".format(os.path.abspath(args.bodyfile)))
    print("")
    print("{}mobile_base:".format("" if args.use_wheel else "# "))
    print("{}  type: geometry_msgs/Twist".format("" if args.use_wheel else "# "))
    print("{}  topic: /{}/cmd_vel".format("" if args.use_wheel else "# ", robotname))
    print("{}  baselink: Root".format("" if args.use_wheel else "# "))
    print("")
    print("joint_groups:")
    print("  -")
    print("    name: default")
    print("    topic: /{}/{}/command".format(robotname,args.controller_name))
    print("    # type: 'action' or 'command'")
    print("    type: command")
    print("    joint_names: {}".format([name for name in jointnames]))
    print("")
    print("devices:")
    print("  -")
    print("    topic: /{}/joint_states".format(robotname))
    print("    class: JointState")
    print("    name: joint_state")
    print("  -")
    print("    topic: /{}/{}/state".format(robotname, args.controller_name))
    print("    class: JointTrajectoryState")
    print("    name: joint_trajectory_state")
    for idx in range(num_device):
        dev = rbody.getDevice(idx)
        print("  -")
        print("    topic: /{}/{}/value".format(robotname, dev.getName()))
        print("    type: {}".format("std_msgs/Float64" if dev.getName().lower().find('color')<0 else "std_msgs/ColorRGBA"))
        print("    name: {}".format(dev.getName()))
        print("    rate: 10")
    