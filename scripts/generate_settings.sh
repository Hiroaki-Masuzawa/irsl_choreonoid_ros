#!/bin/bash

# See http://unix.stackexchange.com/questions/101080/realpath-command-not-found
realpath ()
{
    f=$@;
    if [ -d "$f" ]; then
        base="";
        dir="$f";
    else
        base="/$(basename "$f")";
        dir=$(dirname "$f");
    fi;
    dir=$(cd "$dir" && /bin/pwd);
    echo "$dir$base"
}


BODYFILE=Robot.body
ROSCONTROLFILE=roscontrol_config.yaml
RICONFIGFILE=robotinterface.yaml
WHEELCONFIG=wheel.yaml


USE_WHEEL=False
USE_ARM=True
WHEEL_LIST=()
CONTROLLERS=("joint_controller" "joint_state_controller")

while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--body)
            BODYFILE="$2"
            shift
            shift
            ;;
        --wheel-joint)
            USE_WHEEL=True
            CONTROLLERS+=("wheel_controller")
            shift
            while [[ $# -gt 0 ]]; do
                tmp=$1
                if [ ${tmp:0:1} == "-" ]; then
                    exit
                fi
                WHEEL_LIST+=($tmp)
                shift
            done
            ;;
        
    esac
done

ROBOTNAME=`python3 -c "import cnoid.Body;import sys;print(cnoid.Body.BodyLoader().load('$BODYFILE').getModelName())"`

URDFFILE=`echo $BODYFILE |sed 's/.body$/.urdf/g'`
CNOIDFILE=sim_$ROBOTNAME.cnoid

CHOREONOID_DIR_PATH=$(dirname $(which choreonoid))

wheel_length=${#WHEEL_LIST[@]}
WHEELOPTION=
if [ $wheel_length -gt 0 ] ; then
    WHEELOPTION=--wheeljoints
fi


set -x
choreonoid_body2urdf $BODYFILE > $URDFFILE 2>/dev/null

rosrun irsl_choreonoid_ros generate_roscontroller_config.py --bodyfile $BODYFILE $WHEELOPTION ${WHEEL_LIST[@]} > $ROSCONTROLFILE
CONTROLLERS_LIST=`python3 -c "import yaml; f=open('$ROSCONTROLFILE'); obj=yaml.safe_load(f); f.close(); [ print(str(c)+' ', end='') for c in obj.keys() ]"`

if [ $wheel_length -gt 0 ] ; then
   rosrun irsl_choreonoid_ros generate_wheelconfig.py --bodyfile $BODYFILE --wheeljoints ${WHEEL_LIST[@]} > $WHEELCONFIG
fi

rosrun irsl_choreonoid_ros generate_cnoid.py --bodyfile $BODYFILE --templatefile $CHOREONOID_DIR_PATH/../share/irsl_choreonoid_ros/config/choreonoid_ros_template.cnoid > $CNOIDFILE

if [ $wheel_length -gt 0 ] ; then
rosrun irsl_choreonoid_ros generate_ri_config.py --bodyfile $BODYFILE --use_wheel $USE_WHEEL --wheeljoints ${WHEEL_LIST[@]}  > $RICONFIGFILE
else
rosrun irsl_choreonoid_ros generate_ri_config.py --bodyfile $BODYFILE --use_wheel $USE_WHEEL > $RICONFIGFILE
fi
rosrun irsl_choreonoid_ros generate_roslaunch.py --bodyfile $BODYFILE  --urdffile $URDFFILE --cnoidfile $CNOIDFILE --roscontrolfile $ROSCONTROLFILE --use_wheel $USE_WHEEL --controllers "$CONTROLLERS_LIST" > run_sim_robot.launch 