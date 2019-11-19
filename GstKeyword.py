# -*- coding: utf-8 -*-

"""
  Copyright (C) 2019 Gold Sun Tech Intelligent Technology (Zhejiang) Co., Ltd.
  All Rights Reserved

  Name: GstKeyword.py
  Purpose:

  Created By:    Clive Lau <clivelau@gst-tech.top>
  Created Date:  2019-11-19

  Changelog:
  Date         Desc
  2019-11-19   Created by Clive Lau
"""

# Builtin libraries
# import os
# import time

# Third-party libraries
# import Utils
from robot.api import logger
import usb1

# Custom libraries
from USB2XXX.CommCAN import USB2CAN


class GstKeyword(object):
    def __init__(self):
        self._tag = self.__class__.__name__ + ': '
        logger.debug(self._tag + "__init__ called")

    def is_ready_board_card(self, vid, pid):
        """ 检测板卡是否就绪

        :param vid: 厂商识别号

        :param pid: 产品识别号

        :return: True if ready or not
        """
        logger.info(self._tag + "isExistBoardCard called")
        is_existed = False
        with usb1.USBContext() as context:
            for device in context.getDeviceIterator(skip_on_error=True):
                if (device.getVendorID() == vid) and (device.getProductID() == pid):
                    is_existed = True
        return is_existed

    def request_switch_front_camera(self):
        """ 请求切换前视摄像头

        :return: True if success or not
        """
        can = USB2CAN()
        can.open()
        can.write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00)))
        can.release()

    def request_switch_front_camera(self):
        """ 请求切换前视摄像头

        :return: True if success or not
        """
        can = USB2CAN()
        can.open()
        can.write((int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00), int(0x00)))
        can.release()


if __name__ == '__main__':
    gst = GstKeyword()
    # 检测MCU控制板卡是否就绪
    print(gst.is_ready_board_card(int(0x0483), int(0x7918)))
    # 检测AV采集板卡是否就绪
    print(gst.is_ready_board_card(int(0x5341), int(0x0021)))
    pass
