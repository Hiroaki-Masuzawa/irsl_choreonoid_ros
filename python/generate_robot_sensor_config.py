#!/usr/bin/python3
import argparse
import numpy
import os
import sys

import irsl_choreonoid.cnoid_util as iu

if __name__=='__main__':
    parser = argparse.ArgumentParser(
            prog='generate controller config', # プログラム名
            usage='', # プログラムの利用方法
            add_help=True, # -h/–help オプションの追加
            )
    parser.add_argument('--bodyfile', type=str, default="robotname.body")
    
    args = parser.parse_args()
    fname = args.bodyfile
    rbody = iu.loadRobot(fname)
    
    num_device = rbody.getNumDevices()

    print("I2CHubPublisher:")
    print("    'address': '0x70'")
    for idx in range(num_device):
        dev = rbody.getDevice(idx)
        print("    '{}':".format(idx))
        print("        address: 'XXXX' # Input sensor address. color sensor is 0x70. Other sensor is 0x29.")
        print("        name: XXXX # input sensor type. ex. ColorSensorPublisher, TOFPublisher " )
        print("        topic_name: XXXX/value # Input sensor topic name")