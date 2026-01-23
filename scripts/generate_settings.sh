#!/bin/bash

set -e

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


BODYFILE=''
RICONFIGFILE=robot_interface.yaml
WORLDSETTINGFILE=world.yaml


CONTROLLERS=("trajectory_controller" "joint_state_controller")

while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--body)
            BODYFILE="$2"
            shift
            shift
            ;;
        --help)
            echo "generator_settings.sh [ -b | --body <bodyfile.body> ]"
            exit 0
            ;;
        --)
            shift
            break
            ;;
        *)
            POSITIONAL_ARGS+=("$1") # save positional arg
            shift # past argument
            ;;
    esac
done

if [ -z "$BODYFILE" ]; then
    echo "Please input body file using -b/--body <bodyfile>"
    exit
fi

if [ ! -e "$BODYFILE" ]; then
    echo "BODYFILE ${BODYFILE} does not exist!"
    exit
fi

set -x

URDFFILE=`echo $BODYFILE |sed 's/.body$/.urdf/g'`

choreonoid_body2urdf $BODYFILE > $URDFFILE 2>/dev/null

rosrun irsl_choreonoid_ros generate_ri_config.py --bodyfile $BODYFILE --use_wheel $USE_WHEEL > $RICONFIGFILE

rosrun irsl_choreonoid_ros generate_roslaunch.py --gen_type 2 --bodyfile $BODYFILE --use_wheel False --controllers "joint_controller joint_state_controller" --demo_base_dir `pwd` --urdffile $URDFFILE --worldsettings $WORLDSETTINGFILE > run_sim_robot.launch
rosrun irsl_choreonoid_ros generate_world_config.py  $BODYFILE > $WORLDSETTINGFILE

# generate real robot setting files
rosrun irsl_choreonoid_ros generate_robot_sensor_config.py --bodyfile $BODYFILE > sensor_config.yaml
rosrun irsl_choreonoid_ros generate_dxl_shm_config.py --bodyfile $BODYFILE > dynamixel_config.yaml
rosrun irsl_choreonoid_ros generate_ros_control.py --bodyfile $BODYFILE > ros_control.yaml
rosrun irsl_choreonoid_ros generate_jointlist.py --bodyfile $BODYFILE > jointlist.yaml