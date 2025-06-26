# from tf import transformations
import std_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import MultiArrayLayout, MultiArrayDimension
from std_msgs.msg import  (ByteMultiArray,
                           Float32MultiArray, Float64MultiArray,
                            Int8MultiArray,  Int16MultiArray,  Int32MultiArray,  Int64MultiArray,
                           UInt8MultiArray, UInt16MultiArray, UInt32MultiArray, UInt64MultiArray)
import numpy
from cnoid.IRSLCoords import coordinates

"""
irsl_choreonoid_ros/convert_msgs.py

## ToROSMsg
geometry_msgs.msg.Twist = _to_twist
geometry_msgs.msg.TwistStamped = _to_twist_stamped
geometry_msgs.msg.Accel = _to_accel
geometry_msgs.msg.AccelStamped = _to_accel_stamped
geometry_msgs.msg.Wrench = _to_wrench
geometry_msgs.msg.WrenchStamped = _to_wrench_stamped
geometry_msgs.msg.Vector3 = _to_vector3
geometry_msgs.msg.Vector3Stamped = _to_vector3_stamped
geometry_msgs.msg.Point = _to_point
geometry_msgs.msg.PointStamped = _to_point_stamped
geometry_msgs.msg.Quaternion = _to_quaternion
geometry_msgs.msg.QuaternionStamped = _to_quaternion_stamped
geometry_msgs.msg.Pose = _to_pose
geometry_msgs.msg.PoseStamped = _to_pose_stamped
geometry_msgs.msg.Transform = _to_transform
geometry_msgs.msg.TransformStamped = _to_transform_stamped

## FromROSMsg
geometry_msgs.msg.Twist = _from_twist
geometry_msgs.msg.TwistStamped = _from_twist_stamped
geometry_msgs.msg.Accel = _from_accel
geometry_msgs.msg.AccelStamped = _from_accel_stamped
geometry_msgs.msg.Wrench = _from_wrench
geometry_msgs.msg.WrenchStamped = _from_wrench_stamped
geometry_msgs.msg.Vector3 = _from_vector3
geometry_msgs.msg.Vector3Stamped = _from_vector3_stamped
geometry_msgs.msg.Point = _from_point
geometry_msgs.msg.PointStamped = _from_point_stamped
geometry_msgs.msg.Quaternion = _from_quaternion
geometry_msgs.msg.QuaternionStamped = _from_quaternion_stamped
geometry_msgs.msg.Pose = _from_pose
geometry_msgs.msg.PoseStamped = _from_pose_stamped
geometry_msgs.msg.Transform = _from_transform
geometry_msgs.msg.TransformStamped = _from_transform_stamped

You can check python-expression by converting ros-msg to python-expression

Examples:
    >>>> from irsl_choreonoid_ros.convert_msgs import convertToROSMsg
    >>>> from irsl_choreonoid_ros.convert_msgs import convertFromROSMsg
    >>>> import geometry_msgs.msg
    >>>> vec=convertToROSMsg(fv(0, 1, 2), geometry_msgs.msg.Vector3)
    >>>> pose=convertToROSMsg(coordinates(fv(0, 1, 2)), geometry_msgs.msg.Pose)
    >>>> poses=convertToROSMsg(coordinates(fv(0, 1, 2)), geometry_msgs.msg.PoseStamped, header=std_msgs.msg.Header(stamp=rospy.Time(123)))
    >>>> msg = convertFromROSMsg(poses)

"""
###

def convertToROSMsg(pyexpr, class_rosmsg, **kwargs):
    """
    Converts a Python expression to a ROS message of the specified type.

    Args:
        pyexpr: The Python expression to be converted.
        class_rosmsg: The ROS message class to which the Python expression should be converted.
        **kwargs: Additional keyword arguments to be passed to the conversion function.

    Returns:
        The converted ROS message.

    Raises:
        Exception: If the ROS message class is not found in the conversion function map.
    """
    if not class_rosmsg._md5sum in ____to_function_map__:
        raise Exception('class found')
    return ____to_function_map__[class_rosmsg._md5sum](pyexpr, **kwargs)

def convertFromROSMsg(rosmsg):
    """
    Converts a ROS message to a corresponding format using a predefined mapping.

    Args:
        rosmsg (object): The ROS message to be converted.

    Returns:
        object: The converted message using the corresponding function from `__from_function_map__`.

    Raises:
        Exception: If the ROS message's class MD5 checksum is not found in `__from_function_map__`.

    Notes:
        This function checks if the ROS message's class MD5 checksum exists in the 
        `__from_function_map__` dictionary. If a matching function is found, it is 
        used to convert the ROS message. Otherwise, an exception is raised.

    """
    if not rosmsg.__class__._md5sum in __from_function_map__:
        raise Exception('class found')
    return __from_function_map__[rosmsg.__class__._md5sum](rosmsg)

##geometry_msgs/Vector3
def _to_vector3(pyexpr, **kwargs):
    return geometry_msgs.msg.Vector3(x=pyexpr[0], y=pyexpr[1], z=pyexpr[2])
def _from_vector3(rosmsg):
    return numpy.array((rosmsg.x, rosmsg.y, rosmsg.z), dtype='float64')

##geometry_msgs/Vector3Stamped
def _to_vector3_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.Vector3Stamped(vector=_to_vector3(pyexpr), **kwargs)
def _from_vector3_stamped(rosmsg):
    hdr = rosmsg.header
    res = _from_vector3(rosmsg.vector)
    return (hdr, res)

##geometry_msgs/Quaternion
def _to_quaternion(pyexpr, **kwargs):
    return geometry_msgs.msg.Quaternion(x=pyexpr[0], y=pyexpr[1], z=pyexpr[2], w=pyexpr[3])
def _from_quaternion(rosmsg):
    return numpy.array((rosmsg.x, rosmsg.y, rosmsg.z, rosmsg.w), dtype='float64')

##geometry_msgs/QuaternionStamped
def _to_quaternion_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.QuaternionStamped(quaternion=_to_quaternion(pyexpr), **kwargs)
def _from_quaternion_stamped(rosmsg):
    hdr = rosmsg.header
    res = _from_quaternion(rosmsg.quaternion)
    return (hdr, res)

##geometry_msgs/Point
def _to_point(pyexpr, **kwargs):
    return geometry_msgs.msg.Point(x=pyexpr[0], y=pyexpr[1], z=pyexpr[2])
def _from_point(rosmsg):
    return numpy.array((rosmsg.x, rosmsg.y, rosmsg.z), dtype='float64')

##geometry_msgs/PointStamped
def _to_point_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.PointStamped(point=_to_point(pyexpr), **kwargs)
def _from_point_stamped(rosmsg):
    hdr = rosmsg.header
    res = _from_point(rosmsg.point)
    return (hdr, res)

##geometry_msgs/Pose
def _to_pose(pyexpr, **kwargs):
    return geometry_msgs.msg.Pose(position = _to_point(pyexpr.pos),
                                  orientation = _to_quaternion(pyexpr.quaternion))
def _from_pose(rosmsg):
    return coordinates(_from_point(rosmsg.position), _from_quaternion(rosmsg.orientation))

##geometry_msgs/PoseStamped
def _to_pose_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.PoseStamped(pose = _to_pose(pyexpr), **kwargs)
def _from_pose_stamped(rosmsg):
    return rosmsg.header, _from_pose(rosmsg.pose)

##geometry_msgs/Transform
def _to_transform(pyexpr, **kwargs):
    return geometry_msgs.msg.Transform(translation = _to_vector3(pyexpr.pos),
                                       rotation = _to_quaternion(pyexpr.quaternion))
def _from_transform(rosmsg):
    return coordinates(_from_vector3(rosmsg.translation), _from_quaternion(rosmsg.rotation))

##geometry_msgs/TransformStamped
def _to_transform_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.TransformStamped(transform = _to_transform(pyexpr), **kwargs)
def _from_transform_stamped(rosmsg):
    return rosmsg.header, _from_transform(rosmsg.transform)

# geometry_msgs/Twist
def _to_twist(pyexpr, **kwargs):
    return geometry_msgs.msg.Twist(linear=_to_vector3(pyexpr[0:3]), angular=_to_vector3(pyexpr[3:]))
def _from_twist(rosmsg):
    return numpy.array((rosmsg.linear.x, rosmsg.linear.y, rosmsg.linear.z,
                        rosmsg.angular.x, rosmsg.angular.y, rosmsg.angular.z), dtype='float64')

# geometry_msgs/TwistStamped
def _to_twist_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.TwistStamped(twist = _to_twist(pyexpr), **kwargs)
def _from_twist_stamped(rosmsg):
    return rosmsg.header, _from_twist(rosmsg.twist)

# geometry_msgs/Accel
def _to_accel(pyexpr, **kwargs):
    return geometry_msgs.msg.Accel(linear=_to_vector3(pyexpr[0:3]), angular=_to_vector3(pyexpr[3:]))
def _from_accel(rosmsg):
    return numpy.array((rosmsg.linear.x, rosmsg.linear.y, rosmsg.linear.z,
                        rosmsg.angular.x, rosmsg.angular.y, rosmsg.angular.z), dtype='float64')

# geometry_msgs/AccelStamped
def _to_accel_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.AccelStamped(accel = _to_accel(pyexpr), **kwargs)
def _from_accel_stamped(rosmsg):
    return rosmsg.header, _from_accel(rosmsg.accel)

# geometry_msgs/Wrench
def _to_wrench(pyexpr, **kwargs):
    return geometry_msgs.msg.Wrench(force=_to_vector3(pyexpr[0:3]), torque=_to_vector3(pyexpr[3:]))
def _from_wrench(rosmsg):
    return numpy.array((rosmsg.force.x, rosmsg.force.y, rosmsg.force.z,
                        rosmsg.torque.x, rosmsg.torque.y, rosmsg.torque.z), dtype='float64')

# geometry_msgs/WrenchStamped
def _to_wrench_stamped(pyexpr, **kwargs):
    return geometry_msgs.msg.WrenchStamped(wrench = _to_wrench(pyexpr), **kwargs)
def _from_wrench_stamped(rosmsg):
    return rosmsg.header, _from_wrench(rosmsg.wrench)

##geometry_msgs/PoseWithCovariance
##geometry_msgs/PoseWithCovarianceStamped
##
##geometry_msgs/AccelWithCovariance
##geometry_msgs/AccelWithCovarianceStamped
##
##geometry_msgs/TwistWithCovariance
##geometry_msgs/TwistWithCovarianceStamped
##
##geometry_msgs/Inertia
##geometry_msgs/InertiaStamped
##
## not implemented
##geometry_msgs/Point32
##geometry_msgs/Pose2D
##geometry_msgs/PoseArray
##geometry_msgs/Polygon
##geometry_msgs/PolygonStamped
# std_msgs/ColorRGBA
# nav_msgs/Odom

def checkLayout(MultiArrayLayout_msg):
    dims = MultiArrayLayout_msg.layout.dim
    ## MultiArrayLayout_msg.data_offset
    dim_size = len(dims)
    cur_stride = 1
    for dim in dims[::-1]: ## reverse iterator
        if dim.size < 1:
            raise Exception('dim[{}] == {} is less than 0, ', dim.label, dim.size)
        cur_stride *= dim.size
        if dim.stride != cur_stride:
            raise Exception('dim[{}].stride == {} is not qeual to culculated {}', dim.label, dim.stride, cur_stride)
    return cur_stride - MultiArrayLayout_msg.layout.data_offset

def makeLayout(nparray):
    _shape = nparray.shape
    dim_size = len(_shape)
    cntr = 0
    cur_stride = 1
    dims = []
    for sz in _shape[::-1]: ## reverse iterator
        dim = MultiArrayDimension()
        dim.size   = sz
        cur_stride *= sz
        dim.stride = cur_stride
        dim.label  = 'dim{}'.format(dim_size - cntr)
        dims.append(dim)
        cntr += 1
    return MultiArrayLayout(dim = list(reversed(dims)), data_offset = 0)

def convertToMultiArrayRaw(nparray, ary_cls):
    layout = makeLayout(nparray)
    res = ary_cls(data=nparray.reshape((1, -1))[0].tolist(), layout=layout)
    return res

def convertFromMultiArrayRaw(rosmsg, dtype=None):
    res = numpy.array(rosmsg.data, dtype=dtype)
    return res.reshape([ d.size for d in rosmsg.layout.dim ])

def convertToMultiArray(nparray):
    cls = __NUMPY_to_Msg__[str(nparray.dtype)]
    return convertToMultiArrayRaw(nparray, cls)

def convertFromMultiArray(rosmsg):
    dtype = __Msg_to_NUMPY__[rosmsg._md5sum]
    return convertFromMultiArrayRaw(rosmsg, dtype)

__Msg_to_NUMPY__ = {}
__NUMPY_to_Msg__ = {}
def generateMultiArrayMap():
    __Msg_to_NUMPY__[ByteMultiArray._md5sum   ] = 'uint8'
    __Msg_to_NUMPY__[Float32MultiArray._md5sum] = 'float32'
    __Msg_to_NUMPY__[Float64MultiArray._md5sum] = 'float64'
    __Msg_to_NUMPY__[Int8MultiArray._md5sum   ] = 'int8'
    __Msg_to_NUMPY__[Int16MultiArray._md5sum  ] = 'int16'
    __Msg_to_NUMPY__[Int32MultiArray._md5sum  ] = 'int32'
    __Msg_to_NUMPY__[Int64MultiArray._md5sum  ] = 'int64'
    __Msg_to_NUMPY__[UInt8MultiArray._md5sum  ] = 'uint8'
    __Msg_to_NUMPY__[UInt16MultiArray._md5sum ] = 'uint16'
    __Msg_to_NUMPY__[UInt32MultiArray._md5sum ] = 'uint32'
    __Msg_to_NUMPY__[UInt64MultiArray._md5sum ] = 'uint64'

    __NUMPY_to_Msg__['float32' ]  = Float32MultiArray
    __NUMPY_to_Msg__['float64' ]  = Float64MultiArray
    __NUMPY_to_Msg__['int8'    ]  = Int8MultiArray
    __NUMPY_to_Msg__['int16'   ]  = Int16MultiArray
    __NUMPY_to_Msg__['int32'   ]  = Int32MultiArray
    __NUMPY_to_Msg__['int64'   ]  = Int64MultiArray
    __NUMPY_to_Msg__['uint8'   ]  = UInt8MultiArray
    __NUMPY_to_Msg__['uint16'  ]  = UInt16MultiArray
    __NUMPY_to_Msg__['uint32'  ]  = UInt32MultiArray
    __NUMPY_to_Msg__['uint64'  ]  = UInt64MultiArray

____to_function_map__ = {}
__from_function_map__ = {}
def generateConversionMap():
    ____to_function_map__[ geometry_msgs.msg.Twist._md5sum ] = _to_twist
    __from_function_map__[ geometry_msgs.msg.Twist._md5sum ] = _from_twist
    ____to_function_map__[ geometry_msgs.msg.TwistStamped._md5sum ] = _to_twist_stamped
    __from_function_map__[ geometry_msgs.msg.TwistStamped._md5sum ] = _from_twist_stamped
    ____to_function_map__[ geometry_msgs.msg.Accel._md5sum ] = _to_accel
    __from_function_map__[ geometry_msgs.msg.Accel._md5sum ] = _from_accel
    ____to_function_map__[ geometry_msgs.msg.AccelStamped._md5sum ] = _to_accel_stamped
    __from_function_map__[ geometry_msgs.msg.AccelStamped._md5sum ] = _from_accel_stamped
    ____to_function_map__[ geometry_msgs.msg.Wrench._md5sum ] = _to_wrench
    __from_function_map__[ geometry_msgs.msg.Wrench._md5sum ] = _from_wrench
    ____to_function_map__[ geometry_msgs.msg.WrenchStamped._md5sum ] = _to_wrench_stamped
    __from_function_map__[ geometry_msgs.msg.WrenchStamped._md5sum ] = _from_wrench_stamped
    ____to_function_map__[ geometry_msgs.msg.Vector3._md5sum ] = _to_vector3
    __from_function_map__[ geometry_msgs.msg.Vector3._md5sum ] = _from_vector3
    ____to_function_map__[ geometry_msgs.msg.Vector3Stamped._md5sum ] = _to_vector3_stamped
    __from_function_map__[ geometry_msgs.msg.Vector3Stamped._md5sum ] = _from_vector3_stamped
    ____to_function_map__[ geometry_msgs.msg.Point._md5sum ] = _to_point
    __from_function_map__[ geometry_msgs.msg.Point._md5sum ] = _from_point
    ____to_function_map__[ geometry_msgs.msg.PointStamped._md5sum ] = _to_point_stamped
    __from_function_map__[ geometry_msgs.msg.PointStamped._md5sum ] = _from_point_stamped
    ____to_function_map__[ geometry_msgs.msg.Quaternion._md5sum ] = _to_quaternion
    __from_function_map__[ geometry_msgs.msg.Quaternion._md5sum ] = _from_quaternion
    ____to_function_map__[ geometry_msgs.msg.QuaternionStamped._md5sum ] = _to_quaternion_stamped
    __from_function_map__[ geometry_msgs.msg.QuaternionStamped._md5sum ] = _from_quaternion_stamped
    ____to_function_map__[ geometry_msgs.msg.Pose._md5sum ] = _to_pose
    __from_function_map__[ geometry_msgs.msg.Pose._md5sum ] = _from_pose
    ____to_function_map__[ geometry_msgs.msg.PoseStamped._md5sum ] = _to_pose_stamped
    __from_function_map__[ geometry_msgs.msg.PoseStamped._md5sum ] = _from_pose_stamped
    ____to_function_map__[ geometry_msgs.msg.Transform._md5sum ] = _to_transform
    __from_function_map__[ geometry_msgs.msg.Transform._md5sum ] = _from_transform
    ____to_function_map__[ geometry_msgs.msg.TransformStamped._md5sum ] = _to_transform_stamped
    __from_function_map__[ geometry_msgs.msg.TransformStamped._md5sum ] = _from_transform_stamped

generateConversionMap()
generateMultiArrayMap()
