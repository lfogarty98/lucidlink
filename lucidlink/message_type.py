from enum import IntEnum

class MessageType(IntEnum):
    VERSION_CHECK = 0x0001
    VERSION_REPLY = 0x0002
    DEVICE_STATUS = 0x0003
    REQUEST_DEVICE_STATUS = 0x0004
    REQUEST_SYNCHRONIZATION = 0x0010
    CHANGE_CONFIGURATION = 0x0011
    REQUEST_CURRENT_CONFIGURATION = 0x0100
    SOFT_ERROR = 0xff00
    HARD_ERROR = 0xff01