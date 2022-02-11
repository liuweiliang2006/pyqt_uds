from ctypes import *

# 依赖的DLL文件(存放在根目录下)
CAN_DLL_PATH = './ControlCAN.dll'

# 读取DLL文件
Can_DLL = windll.LoadLibrary(CAN_DLL_PATH)

# CAN卡类别为 USBCAN-2A, USBCAN-2C, CANalyst-II
VCI_USB_CAN_2 = 4

# CAN卡下标索引, 比如当只有一个USB-CAN适配器时, 索引号为0, 这时再插入一个USB-CAN适配器那么后面插入的这个设备索引号就是1, 以此类推
DEV_INDEX = 0


# 打开设备, 一个设备只能打开一次
# return: 1=OK 0=ERROR
def connect():
    # VCI_USB_CAN_2: 设备类型
    # DEV_INDEX:     设备索引
    # RESERVED:      保留参数
    ret = Can_DLL.VCI_OpenDevice(VCI_USB_CAN_2, DEV_INDEX, RESERVED)
    if ret == STATUS_OK:
        print('VCI_OpenDevice: 设备开启成功')
    else:
        print('VCI_OpenDevice: 设备开启失败')
    return ret


# 通道初始化参数结构
# AccCode:  过滤验收码
# AccMask:  过滤屏蔽码
# Reserved: 保留字段
# Filter:   滤波模式 0/1=接收所有类型 2=只接收标准帧 3=只接收扩展帧
# Timing0:  波特率 T0
# Timing1:  波特率 T1
# Mode:     工作模式 0=正常工作 1=仅监听模式 2=自发自收测试模式
class VCI_CAN_INIT_CONFIG(Structure):
    _fields_ = [
        ("AccCode", c_uint),
        ("AccMask", c_uint),
        ("Reserved", c_uint),
        ("Filter", c_ubyte),
        ("Timing0", c_ubyte),
        ("Timing1", c_ubyte),
        ("Mode", c_ubyte)
    ]


# 过滤验收码
ACC_CODE = 0x80000000

# 过滤屏蔽码
ACC_MASK = 0xFFFFFFFF

# 保留字段
RESERVED = 0

# 滤波模式 0/1=接收所有类型
FILTER = 0

# 波特率 T0
TIMING_0 = 0x03

# 波特率 T1
TIMING_1 = 0x1C

# 工作模式 0=正常工作
MODE = 0

STATUS_OK =1
# 初始化通道
# return: 1=OK 0=ERROR
def init(can_index):
    init_config = VCI_CAN_INIT_CONFIG(ACC_CODE, ACC_MASK, RESERVED, FILTER, TIMING_0, TIMING_1, MODE)
    # VCI_USB_CAN_2: 设备类型
    # DEV_INDEX:     设备索引
    # can_index:     CAN通道索引
    # init_config:   请求参数体
    ret = Can_DLL.VCI_InitCAN(VCI_USB_CAN_2, DEV_INDEX, can_index, byref(init_config))
    if ret == STATUS_OK:
        print('VCI_InitCAN: 通道 ' + str(can_index + 1) + ' 初始化成功')
    else:
        print('VCI_InitCAN: 通道 ' + str(can_index + 1) + ' 初始化失败')
    return ret

if __name__ == '__main__':
    connect()
    # 初始化CAN1
    # init(CAN_INDEX_1)
    # # 启动CAN1
    # start(CAN_INDEX_1)
    # # 初始化CAN2
    # init(CAN_INDEX_2)
    # # 启动CAN2
    # start(CAN_INDEX_2)
    # # CAN1发送数据
    # transmit(CAN_INDEX_1)
    # # CAN2接收数据
    # receive(CAN_INDEX_2)