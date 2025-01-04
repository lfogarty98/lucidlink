from enum import IntEnum

class MessageType(IntEnum):
    VERSION_CHECK = 1
    VERSION_REPLY = 2
    DEVICE_STATUS = 3
    REQUEST_DEVICE_STATUS = 4