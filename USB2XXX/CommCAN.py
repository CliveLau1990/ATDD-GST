# -*- coding: utf-8 -*-

"""
  Copyright (C) 2019 Gold Sun Tech Intelligent Technology (Zhejiang) Co., Ltd.
  All Rights Reserved

  Name: CommCAN.py
  Purpose:

  Created By:    Clive Lau <clivelau@gst-tech.top>
  Created Date:  2019-11-19

  Changelog:
  Date         Desc
  2019-11-19   Created by Clive Lau
"""

# Builtin libraries
from ctypes import *
import platform
from time import sleep

# Third-party libraries
from robot.api import logger
from usb_device import *
from usb2can import *

# Custom libraries


class USB2CAN(object):
    def __init__(self):
        self._tag = self.__class__.__name__ + ': '
        self.index_can = 0
        self.dev_handles = (c_uint * 20)()

    def open(self):
        # Scan device
        ret = USB_ScanDevice(byref(self.dev_handles))
        if ret == 0:
            logger.error(self._tag + "No device connected!")
            exit()
        else:
            logger.info(self._tag + "Have %d device connected!" % ret)
        # Open device
        ret = USB_OpenDevice(self.dev_handles[0])
        if not bool(ret):
            logger.error(self._tag + "Open device faild!")
            exit()
        else:
            logger.info(self._tag + "Open device success!")
        # 初始化CAN
        CANConfig = CAN_INIT_CONFIG()
        # 1-自发自收模式，0-正常模式
        CANConfig.CAN_Mode = 0
        CANConfig.CAN_ABOM = 0
        CANConfig.CAN_NART = 1
        CANConfig.CAN_RFLM = 0
        CANConfig.CAN_TXFP = 1
        # 配置波特率,波特率 = 100M/(BRP*(SJW+BS1+BS2))
        CANConfig.CAN_BRP_CFG3 = 25
        CANConfig.CAN_BS1_CFG1 = 6
        CANConfig.CAN_BS2_CFG2 = 1
        CANConfig.CAN_SJW = 1
        ret = CAN_Init(self.dev_handles[0], self.index_can, byref(CANConfig))
        if ret != CAN_SUCCESS:
            logger.error(self._tag + "Config CAN failed!")
            exit()
        else:
            logger.info(self._tag + "Config CAN Success!")
        # 配置过滤器，必须配置，否则可能无法收到数据
        CANFilter = CAN_FILTER_CONFIG()
        CANFilter.Enable = 1
        CANFilter.ExtFrame = 0
        CANFilter.FilterIndex = 0
        CANFilter.FilterMode = 0
        CANFilter.MASK_IDE = 0
        CANFilter.MASK_RTR = 0
        CANFilter.MASK_Std_Ext = 0
        ret = CAN_Filter_Init(self.dev_handles[0], self.index_can, byref(CANFilter))
        if ret != CAN_SUCCESS:
            logger.error(self._tag + "Config CAN Filter failed!")
            exit()
        else:
            logger.info(self._tag + "Config CAN Filter Success!")

    def release(self):
        # Close device
        ret = USB_CloseDevice(self.dev_handles[0])
        if not bool(ret):
            logger.error(self._tag + "Close device faild!")
            exit()
        else:
            logger.info(self._tag + "Close device success!")

    def write(self, payload):
        # 发送CAN帧
        CanMsg = (CAN_MSG * 1)()
        CanMsg[0].ExternFlag = 0
        CanMsg[0].RemoteFlag = 0
        CanMsg[0].ID = int(0x05a0)
        CanMsg[0].DataLen = 8
        for idx in range(0, CanMsg[0].DataLen):
            CanMsg[0].Data[idx] = payload[idx]
        SendedNum = CAN_SendMsg(self.dev_handles[0], self.index_can, byref(CanMsg), 1)
        if SendedNum >= 0:
            print("Success send frames:%d" % SendedNum)
        else:
            print("Send CAN data failed!")


if __name__ == '__main__':
    can = USB2CAN()
    can.open()
    # 前视摄像头
    can.write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00)))
    # 左视摄像头
    # can.write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x01)))
    # 右视摄像头
    # can.write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x02)))
    # 后视摄像头
    # can.write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x03)))
    can.release()
    pass
