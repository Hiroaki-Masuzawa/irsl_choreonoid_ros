#!/usr/bin/python3
import pathlib
import argparse
import yaml

import irsl_choreonoid.cnoid_util as iu

from generate_utils import get_jointnamelist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='generage world setting file',  # プログラム名
        usage='Generate world setting for choreonoidros',  # プログラムの利用方法
        add_help=True,  # -h/–help オプションの追加
    )
    parser.add_argument('bodyfile', type=str, default="robotname.body")
    parser.add_argument('--robotname', type=str, default="")
    parser.add_argument('--offsetx', type=float, default="0.0")
    parser.add_argument('--offsety', type=float, default="0.0")
    parser.add_argument('--offsetz', type=float, default="0.0")
    parser.add_argument('--joint_controller_name', type=str, default="joint_controller")
    args = parser.parse_args()

    fname = str(args.bodyfile)
    rbody = iu.loadRobot(fname)
    jointnames = get_jointnamelist(rbody)

    p = pathlib.Path(args.bodyfile)
    bodyfile_path = str(p.resolve())
    robotname = args.robotname if args.robotname != "" else rbody.getModelName()

    world_config = {'robot':
                    {
                        'model': bodyfile_path,
                        'name': robotname,
                        'initial_coords': {'pos': [args.offsetx, args.offsety, args.offsetz]},
                        'initial_joint_angles': [0 for _ in range(len(jointnames))],
                        'fix': True,
                        'BodyROSItem': {'name_space': robotname},
                        'ROSControlItem': {'name_space': robotname}
                    },
                    'world':
                    {
                        'World': {'name': 'MyWorld'},
                        'Simulator': {
                            'type': 'AISTSimulator',
                            'name': 'AISTSim'
                        },
                        'GLVision': None,
                        'Camera': {
                            'lookEye': [0.0, 3.0, 1.7],
                            'lookUp': [0.0, 0.0, 1.0],
                            'lookAtCenter': [0.0, 0.0, 0.7]
                        },
                        'WorldROS': None,
                        'ROS': {
                            'generate': {'robot': bodyfile_path,
                                         'name_space': robotname,
                                         'controllers': [
                                             {
                                                 'name': args.joint_controller_name,
                                                 'type': 'position',
                                                 'joints': sorted([name for name in jointnames])
                                             }
                                         ]
                                         }
                        }
                    },
                    'objects': [
                        {
                            'model': 'choreonoid://share/model/misc/floor.body',
                            'name': 'MyFloor',
                            'fix': True
                        }
                    ]
                    }

    print(yaml.dump(world_config, indent=2, sort_keys=False))
