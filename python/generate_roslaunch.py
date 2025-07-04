#!/usr/bin/python3
import argparse
import numpy
import os
import sys

from distutils.util import strtobool

try:
    import cnoid.Body
    import cnoid.Util
except ImportError:
    import sys
    import shutil
    choreonoid_bin_path = shutil.which('choreonoid')
    if choreonoid_bin_path is None:
        print('Error: choreonoid is not found.', file=sys.stderr)
        sys.exit(1)
    choreonoid_bin_dir_path = os.path.dirname(choreonoid_bin_path)
    choreonoid_share_path = os.path.join(choreonoid_bin_dir_path, '../share')
    chorenoid_ver = [dirname[dirname.find('choreonoid-')+len('choreonoid-'):] for dirname in os.listdir(choreonoid_share_path) if dirname.find('choreonoid-') != -1]
    if len(chorenoid_ver) > 0:
        chorenoid_ver = chorenoid_ver[0]
    else :
        chorenoid_ver = None
    choreonoid_python_path = os.path.join(choreonoid_bin_dir_path, '../lib/choreonoid-{}/python'.format(chorenoid_ver))
    print(choreonoid_python_path)
    if choreonoid_python_path is None or not os.path.exists(choreonoid_python_path):
        print('Error: choreonoid_python_path not found.', file=sys.stderr)
        sys.exit(1)
    sys.path.append(choreonoid_python_path)
    import cnoid.Body
    import cnoid.Util


if __name__=='__main__':
    parser = argparse.ArgumentParser(
            prog='generate_roslaunch.py', # プログラム名
            usage='Demonstration of cnoid_dump_model', # プログラムの利用方法

            add_help=True, # -h/–help オプションの追加
            )
    parser.add_argument('--gen_type', type=int, required=True, default=2, choices=[1,2])
    parser.add_argument('--bodyfile', type=str, required=True)
    parser.add_argument('--use_wheel', type=strtobool, default=False)
    parser.add_argument('--controllers', type=str, default='joint_controller joint_state_controller')
    parser.add_argument('--demo_base_dir', type=str, default='/userdir')
    parser.add_argument('--urdffile', type=str, required=True)
    parser.add_argument('--roscontrolfile', type=str)
    parser.add_argument('--cnoidfile', type=str)
    parser.add_argument('--worldsettings', type=str)
    
    args = parser.parse_args()
    fname = args.bodyfile
    if not os.path.isfile(str(fname)):
        print("File is not exist.", file=sys.stderr)
        print("Please check file : {}".format(fname), file=sys.stderr)
        exit(1)
    rbody = cnoid.Body.BodyLoader().load(str(fname))
    if rbody is None:
        print("File is broken.", file=sys.stderr)
        print("Please check file : {}".format(fname), file=sys.stderr)
        exit(1)
    
    rbody.updateLinkTree()
    rbody.initializePosition()
    rbody.calcForwardKinematics()

    joint_list = []

    num_link = rbody.getNumLinks()
    num_joint = rbody.getNumJoints()
    num_device = rbody.getNumDevices()

    for idx in range(num_joint):
        joint = rbody.getJoint(idx)
        joint_list.append(joint)

    robotname = rbody.getModelName()
    
    if args.gen_type == 1:
        print('<launch>')
        print('  <arg name="demo_base_dir" default="/userdir"/>')
        print('  <!-- choreonoid -->')
        print('  <arg name="project_file" default="$(arg demo_base_dir)/{}"/>'.format(args.cnoidfile))
        print('  <arg name="robot_name" default="{}"/>'.format(robotname))
        print('  <!-- ros_control -->')
        print('  <arg name="model" default="$(arg demo_base_dir)/{}"/>'.format(args.urdffile))
        print('  <arg name="control_config" default="$(arg demo_base_dir)/{}"/>'.format(args.roscontrolfile))
        print('  <arg name="controllers" default="{}" />'.format(args.controllers))
        # print('  <!-- joint_controller wheel_controller joint_state_controller -->')
        if args.use_wheel:
            print('  <!-- wheel -->')
            print('  <arg name="wheelconfigfile" default="$(arg demo_base_dir)/wheel.yaml"/>')
        print('')
        print('  <include file="$(find irsl_choreonoid_ros)/launch/sim_robot.launch">')
        print('    <arg name="project_file" value="$(arg project_file)" />')
        print('    <arg name="robot_name" default="$(arg robot_name)"/>')
        print('    <arg name="model" value="$(arg model)" />')
        print('    <arg name="control_config" value="$(arg control_config)" />')
        print('    <arg name="controllers" value="$(arg controllers)" />')
        print('  </include>')
        print('')
        print('  <group ns="$(arg robot_name)" >')
        for idx in range(num_device):
            dev = rbody.getDevice(idx)
            if dev.getName().lower().find('tof')>=0 or dev.getName().lower().find('ultra')>=0 :
                print('    <node name="tof_converter_node_{}" pkg="irsl_choreonoid_ros" type="tof_converter_node.py" output="screen">'.format(idx))
                print('      <remap from="input_points" to="{}/point_cloud"/>'.format(dev.getName()))
                print('      <remap from="output_sensor_data" to="{}/value"/>'.format(dev.getName()))
                print('    </node>')
                print('')
            elif dev.getName().lower().find('color')>=0:
                print('    <node name="colorsensor_converter_node_{}" pkg="irsl_choreonoid_ros" type="colorsensor_converter_node.py" output="screen">'.format(idx))
                print('      <remap from="input_image" to="{}/color/image_raw"/>'.format(dev.getName()))
                print('      <remap from="output_sensor_data" to="{}/value"/>'.format(dev.getName()))
                print('    </node>')
                print('')
        if args.use_wheel:
            print('    <node name="wheelcontroller_node" pkg="irsl_choreonoid_ros" type="wheelcontroller.py" output="screen">')
            print('      <param name="wheelconfigfile" value="$(arg wheelconfigfile)" />')
            print('    </node>')
        print('  </group>')
        print('</launch>')
    elif args.gen_type == 2:
        print('<launch>')
        print('  <arg name="demo_base_dir" default="{}"/>'.format(args.demo_base_dir))
        print('  <!-- choreonoid -->')
        print('  <arg name="worldsettings" default="{}" />'.format(args.worldsettings))
        print('  <arg name="robot_name" default="{}"/>'.format(robotname))
        print('  <!-- ros_control -->')
        print('  <arg name="model" default="$(arg demo_base_dir)/{}"/>'.format(args.urdffile))
        print('  <arg name="controllers" default="{}" />'.format(args.controllers))
        if args.use_wheel:
            print('  <!-- wheel -->')
            print('  <arg name="wheelconfigfile" default="$(arg demo_base_dir)/wheel.yaml"/>')
        print('')
        print('  <include file="$(find irsl_choreonoid_ros)/launch/run_sim_with_setup_cnoid.launch">')
        print('    <arg name="controllers" value="$(arg controllers)" />')
        print('    <arg name="setup_cnoid" value="$(arg demo_base_dir)/$(arg worldsettings)" />')
        print('    <arg name="model_file" value="$(arg model)" />')
        print('    <arg name="model_namespace" value="{}" />'.format(robotname))
        print('    <arg name="control_namespace" value="{}" />'.format(robotname))
        print('  </include>')
        print('')
        print('  <group ns="$(arg robot_name)" >')
        for idx in range(num_device):
            dev = rbody.getDevice(idx)
            if dev.getName().lower().find('tof')>=0 or dev.getName().lower().find('ultra')>=0 :
                print('    <node name="tof_converter_node_{}" pkg="irsl_choreonoid_ros" type="tof_converter_node.py" output="screen">'.format(idx))
                print('      <remap from="input_points" to="{}/point_cloud"/>'.format(dev.getName()))
                print('      <remap from="output_sensor_data" to="{}/value"/>'.format(dev.getName()))
                print('    </node>')
                print('')
            elif dev.getName().lower().find('color')>=0:
                print('    <node name="colorsensor_converter_node_{}" pkg="irsl_choreonoid_ros" type="colorsensor_converter_node.py" output="screen">'.format(idx))
                print('      <remap from="input_image" to="{}/color/image_raw"/>'.format(dev.getName()))
                print('      <remap from="output_sensor_data" to="{}/value"/>'.format(dev.getName()))
                print('    </node>')
                print('')
        if args.use_wheel:
            print('    <node name="wheelcontroller_node" pkg="irsl_choreonoid_ros" type="wheelcontroller.py" output="screen">')
            print('      <param name="wheelconfigfile" value="$(arg wheelconfigfile)" />')
            print('    </node>')
        print('  </group>')
        print('</launch>')
