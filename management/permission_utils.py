class DefaultPermissions:
    # General Purpose
    CAN_READ = 1 << 1
    CAN_WRITE = 2 << 1 | CAN_READ

    # For Chat System
    CREATE_REMOVE_CHANNELS = 3 << 1
    REACT_ON_CHANNEL = 4 << 1
    DELETE_MESSAGES = 5 << 1

    # Cloud space
    CAN_UPLOAD_FILES = 5 << 1
    CAN_DOWNLOAD_FILES = 6 << 1
    ADMIN = CAN_WRITE | CREATE_REMOVE_CHANNELS | REACT_ON_CHANNEL | CAN_UPLOAD_FILES | CAN_DOWNLOAD_FILES
