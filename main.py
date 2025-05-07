#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from main_window import HackerConsole

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用程序名称和组织
    app.setApplicationName("Hacker Simulator")
    app.setOrganizationName("BlackHat")
    
    # 创建并显示主窗口
    main_window = HackerConsole()
    main_window.show()
    
    sys.exit(app.exec_()) 