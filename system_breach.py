#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QProgressBar, QPushButton, QFrame, QGridLayout,
                            QTextEdit, QApplication, QDesktopWidget, QComboBox, QLineEdit)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QBrush, QTextCharFormat, QTextCursor

# 样式常量
BG_COLOR = "#000000"
TEXT_COLOR = "#00FF00"
ACCENT_COLOR = "#00FFAA"
HIGHLIGHT_COLOR = "#FF0000"
ERROR_COLOR = "#FF3333"
SUCCESS_COLOR = "#33FF33"
DEFAULT_FONT = "Consolas"
DEFAULT_FONT_SIZE = 14  # 增大默认字体大小

# 系统名称列表，用于预设目标选择
TARGET_SYSTEMS = [
    "NSA Mainframe",
    "Pentagon Database",
    "FBI Secured Server",
    "CIA Intel Network",
    "Military Defense System",
    "Global Banking Network",
    "Corporate Security System",
    "Government Infrastructure",
    "Satellite Control System",
    "Nuclear Facility Access"
]

# 加密算法列表，用于显示
ENCRYPTION_ALGORITHMS = [
    "AES-256",
    "RSA-4096",
    "Blowfish",
    "3DES",
    "Twofish",
    "IDEA",
    "RC6",
    "Serpent",
    "GOST",
    "CAST-256"
]

# 解密阶段
BREACH_PHASES = [
    "初始化攻击向量...",
    "分析加密算法...",
    "生成解密密钥...",
    "绕过安全措施...",
    "破解防火墙...",
    "绕过入侵检测系统...",
    "注入Shell代码...",
    "提升权限...",
    "覆盖访问日志...",
    "建立隐蔽后门..."
]


class BreachThread(QThread):
    """执行系统入侵的后台线程"""
    
    # 自定义信号
    update_progress = pyqtSignal(int)
    update_status = pyqtSignal(str, str)  # 文本, 类型(info/warning/error/success)
    breach_complete = pyqtSignal(bool)  # 成功/失败
    update_data_viewer = pyqtSignal()  # 更新数据查看器的信号
    
    def __init__(self, target_system, parent=None):
        super().__init__(parent)
        self.target_system = target_system
        self.is_running = True
        
        # 为每次入侵生成随机信息
        self.backdoor_path = f"/var/{random.choice(['www', 'tmp', 'opt', 'log'])}/{random.choice(['system', 'admin', 'server', 'hidden'])}.{random.choice(['php', 'cgi', 'so', 'bin'])}"
        self.exploit_method = random.choice([
            f"CVE-{random.randint(2019, 2023)}-{random.randint(1000, 9999)} 远程代码执行漏洞",
            f"未修补的 {random.choice(['SSH', 'FTP', 'HTTP', 'RDP', 'SMB'])} 服务漏洞",
            "缓冲区溢出攻击",
            "SQL注入攻击链",
            "跨站请求伪造组合攻击",
            "内存错误利用",
            "特权提升漏洞",
            "零日安全漏洞利用",
            f"{random.choice(['认证', '授权', '加密', '输入验证'])}缺陷利用"
        ])
        
        # 生成随机IP地址作为跳板
        self.proxy_servers = []
        for _ in range(random.randint(2, 5)):
            ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            self.proxy_servers.append(ip)
    
    def stop(self):
        """停止入侵过程"""
        self.is_running = False
    
    def run(self):
        """执行入侵操作"""
        # 入侵总共有10个阶段
        total_phases = 10
        
        # 随机确定是否成功(80%成功率)
        will_succeed = random.random() < 0.8
        
        # 如果将会失败，随机决定在哪个阶段失败
        fail_phase = random.randint(5, 9) if not will_succeed else -1
        
        # 告诉主窗口开始更新数据显示
        self.update_data_viewer.emit()
        
        # 执行各阶段
        for i in range(total_phases):
            if not self.is_running:
                return
            
            # 当前阶段进度
            phase_progress = i * 10
            self.update_progress.emit(phase_progress)
            
            # 更新状态
            self.update_status.emit(f"阶段 {i+1}/{total_phases}: {BREACH_PHASES[i]}", "info")
            
            # 模拟工作过程
            for j in range(10):
                if not self.is_running:
                    return
                
                # 更新进度
                progress = phase_progress + j
                self.update_progress.emit(progress)
                
                # 如果是失败阶段的最后一步，发送失败信号
                if i == fail_phase and j == 9:
                    self.update_status.emit(f"错误: 检测到入侵防御系统! 连接断开...", "error")
                    time.sleep(1)
                    self.breach_complete.emit(False)
                    return
                
                # 随机显示一些技术细节
                if random.random() < 0.3:
                    tech_details = [
                        f"正在解析 {random.randint(1000, 9999)} 字节数据块...",
                        f"绕过 {random.choice(ENCRYPTION_ALGORITHMS)} 加密...",
                        f"发现 {random.randint(1, 5)} 个安全漏洞...",
                        f"注入负载: 0x{random.randint(0, 0xFFFFFF):06x}...",
                        f"分析 {random.randint(10, 99)} 个防火墙规则...",
                        f"解密 {random.randint(10, 999)}MB 数据...",
                        f"TCP/IP 数据包碎片化: {random.randint(1, 9)}/{random.randint(10, 20)}...",
                        f"SSH隧道创建: {random.randint(75, 99)}% 完成..."
                    ]
                    self.update_status.emit(random.choice(tech_details), "info")
                
                # 偶尔显示警告
                if random.random() < 0.1 and i > 3:
                    warnings = [
                        "检测到IDS活动，正在规避...",
                        "发现防病毒扫描，启动隐身模式...",
                        "系统日志监控已激活，正在绕过...",
                        "检测到异常流量分析，分散攻击向量...",
                        "管理员可能在线，减慢攻击频率..."
                    ]
                    self.update_status.emit(random.choice(warnings), "warning")
                
                # 模拟延迟
                time.sleep(random.uniform(0.1, 0.3))
        
        # 完成所有阶段
        if self.is_running:
            self.update_progress.emit(100)
            self.update_status.emit(f"入侵成功: 获得对{self.target_system}的完全访问权限!", "success")
            time.sleep(1)
            self.breach_complete.emit(True)


class HexViewer(QTextEdit):
    """十六进制查看器控件，显示模拟的内存/数据转储"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.active = False
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.updateRandomSection)
    
    def initUI(self):
        """初始化界面"""
        self.setReadOnly(True)
        self.setFont(QFont(DEFAULT_FONT, 12))  # 增大字体
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                selection-background-color: {ACCENT_COLOR};
                selection-color: {BG_COLOR};
            }}
        """)
        self.setText("数据查看器将在入侵开始后显示目标系统数据")
    
    def start(self):
        """开始显示和更新数据"""
        self.active = True
        self.updateData()
        self.update_timer.start(500)  # 每500ms更新一次
    
    def stop(self):
        """停止数据更新"""
        self.active = False
        self.update_timer.stop()
    
    def updateData(self):
        """更新显示数据"""
        if not self.active:
            return
            
        self.clear()
        cursor = self.textCursor()
        
        # 生成16行模拟的十六进制数据
        for i in range(16):
            # 地址
            addr_format = QTextCharFormat()
            addr_format.setForeground(QBrush(QColor("#AAAAAA")))
            cursor.insertText(f"{i*16:08x}:  ", addr_format)
            
            # 十六进制数据
            for j in range(16):
                val = random.randint(0, 255)
                
                # 使用不同颜色
                format = QTextCharFormat()
                if val == 0:
                    format.setForeground(QBrush(QColor("#555555")))
                elif val < 32:
                    format.setForeground(QBrush(QColor("#FF5555")))
                elif val < 128:
                    format.setForeground(QBrush(QColor("#55FF55")))
                else:
                    format.setForeground(QBrush(QColor("#5555FF")))
                
                cursor.insertText(f"{val:02x} ", format)
            
            # ASCII表示
            cursor.insertText("  |  ")
            for j in range(16):
                val = random.randint(32, 126)  # 可打印字符
                cursor.insertText(chr(val))
            
            cursor.insertText("\n")
    
    def updateRandomSection(self):
        """随机更新部分数据，制造活动效果"""
        if not self.active:
            return
            
        cursor = self.textCursor()
        
        # 随机选择一行
        line = random.randint(0, 15)
        
        # 定位到该行
        cursor.movePosition(QTextCursor.Start)
        for _ in range(line):
            cursor.movePosition(QTextCursor.Down)
        
        # 移到十六进制数据开始位置
        cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, 10)
        
        # 随机更新几个字节
        num_bytes = random.randint(1, 8)
        for _ in range(num_bytes):
            # 随机选择位置
            pos = random.randint(0, 15)
            cursor.movePosition(QTextCursor.Start)
            for _ in range(line):
                cursor.movePosition(QTextCursor.Down)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, 10 + pos*3)
            
            # 选择3个字符(包括空格)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 3)
            
            # 插入新值
            val = random.randint(0, 255)
            format = QTextCharFormat()
            
            # 高亮更新的值
            format.setForeground(QBrush(QColor("#FFFF55")))
            format.setBackground(QBrush(QColor("#552200")))
            
            # 移除所选并插入新文本
            cursor.removeSelectedText()
            cursor.insertText(f"{val:02x} ", format)


class SystemBreachWindow(QWidget):
    """系统入侵模拟窗口"""
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
        self.initUI()
        self.breach_thread = None
        self.drag_position = None
        
        # 开始闪烁计时器
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggleBlink)
        self.blink_timer.start(500)
        self.blink_on = False
        
        # 更新时钟
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.updateClock)
        self.clock_timer.start(1000)
        
        # 设置窗口位置在左下角
        self.positionWindow()
    
    def initUI(self):
        """初始化界面"""
        # 设置窗口大小 - 增大尺寸
        self.resize(1000, 700)
        self.setWindowTitle("System Breach")
        
        # 设置窗口样式
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: {DEFAULT_FONT};
                border: 1px solid {TEXT_COLOR};
            }}
            QLabel {{
                border: none;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QProgressBar {{
                border: 1px solid {TEXT_COLOR};
                border-radius: 0px;
                text-align: center;
                background-color: {BG_COLOR};
                font-size: {DEFAULT_FONT_SIZE}px;
                min-height: 25px;
            }}
            QProgressBar::chunk {{
                background-color: {TEXT_COLOR};
            }}
            QPushButton {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                padding: 5px;
                min-height: 30px;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 255, 170, 30%);
                color: white;
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 255, 170, 50%);
            }}
            QTextEdit {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                font-family: {DEFAULT_FONT};
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QComboBox {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                padding: 5px;
                min-height: 30px;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                width: 0px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                selection-background-color: {ACCENT_COLOR};
                selection-color: {BG_COLOR};
            }}
            QLineEdit {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                padding: 5px;
                min-height: 30px;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
        """)
        
        # 设置窗口半透明
        self.setWindowOpacity(0.95)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # 顶部标题和关闭按钮
        title_layout = QHBoxLayout()
        
        self.title_label = QLabel("SYSTEM BREACH MODULE v2.0")
        self.title_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold; font-size: 16px;")
        title_layout.addWidget(self.title_label)
        
        title_layout.addStretch()
        
        # 时钟显示
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet(f"color: {TEXT_COLOR}; font-family: {DEFAULT_FONT}; font-size: 14px;")
        title_layout.addWidget(self.clock_label)
        
        title_layout.addSpacing(20)
        
        close_button = QPushButton("×")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {TEXT_COLOR};
                border: none;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {HIGHLIGHT_COLOR};
            }}
        """)
        close_button.clicked.connect(self.close)
        title_layout.addWidget(close_button)
        
        main_layout.addLayout(title_layout)
        
        # 添加水平分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(f"background-color: {TEXT_COLOR};")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)
        
        # 目标系统选择区域
        target_layout = QHBoxLayout()
        
        target_label = QLabel("目标系统:")
        target_label.setStyleSheet("border: none; font-weight: bold; font-size: 14px;")
        target_layout.addWidget(target_label)
        
        # 添加下拉菜单
        self.target_combo = QComboBox()
        for target in TARGET_SYSTEMS:
            self.target_combo.addItem(target)
        self.target_combo.setCurrentIndex(random.randint(0, len(TARGET_SYSTEMS)-1))
        self.target_combo.setEditable(True)
        self.target_combo.setFixedWidth(300)
        target_layout.addWidget(self.target_combo)
        
        target_layout.addStretch()
        
        # 状态指示器
        self.status_indicator = QLabel("● 待命")
        self.status_indicator.setStyleSheet(f"color: {TEXT_COLOR}; border: none; font-size: 14px;")
        target_layout.addWidget(self.status_indicator)
        
        main_layout.addLayout(target_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        main_layout.addWidget(self.progress_bar)
        
        # 中央区域
        central_layout = QHBoxLayout()
        
        # 左侧日志区域
        log_layout = QVBoxLayout()
        
        log_label = QLabel("操作日志")
        log_label.setStyleSheet("border: none; font-weight: bold; font-size: 14px;")
        log_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        central_layout.addLayout(log_layout, 3)  # 分配更多空间给日志
        
        # 右侧数据查看器
        data_layout = QVBoxLayout()
        
        data_label = QLabel("数据查看器")
        data_label.setStyleSheet("border: none; font-weight: bold; font-size: 14px;")
        data_layout.addWidget(data_label)
        
        self.hex_viewer = HexViewer()
        data_layout.addWidget(self.hex_viewer)
        
        central_layout.addLayout(data_layout, 2)
        
        main_layout.addLayout(central_layout)
        
        # 底部按钮区域
        button_layout = QHBoxLayout()
        
        self.breach_button = QPushButton("开始入侵")
        self.breach_button.clicked.connect(self.toggle_breach)
        button_layout.addWidget(self.breach_button)
        
        self.clear_button = QPushButton("清除日志")
        self.clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # 设置布局
        self.setLayout(main_layout)
        
        # 鼠标追踪
        self.setMouseTracking(True)
    
    def positionWindow(self):
        """设置窗口位置在左下角"""
        desktop = QDesktopWidget().availableGeometry()
        self.move(20, desktop.height() - self.height() - 40)
    
    def updateClock(self):
        """更新时钟显示"""
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.clock_label.setText(current_time)
    
    def toggleBlink(self):
        """切换闪烁状态"""
        self.blink_on = not self.blink_on
        
        if self.breach_thread and self.breach_thread.isRunning():
            if self.blink_on:
                self.status_indicator.setStyleSheet(f"color: #FF0000; border: none; font-size: 14px;")
                self.status_indicator.setText("● 正在入侵")
            else:
                self.status_indicator.setStyleSheet(f"color: transparent; border: none; font-size: 14px;")
                self.status_indicator.setText("○ 正在入侵")
    
    def toggle_breach(self):
        """切换入侵状态"""
        if self.breach_thread and self.breach_thread.isRunning():
            # 停止入侵
            self.breach_thread.stop()
            self.breach_button.setText("开始入侵")
            self.status_indicator.setStyleSheet(f"color: {TEXT_COLOR}; border: none; font-size: 14px;")
            self.status_indicator.setText("● 已中止")
            self.add_log("入侵操作已手动终止", "warning")
            self.hex_viewer.stop()
            self.target_combo.setEnabled(True)
        else:
            # 开始入侵
            self.start_breach()
    
    def start_breach(self):
        """开始入侵操作"""
        # 获取用户选择的目标系统
        target_system = self.target_combo.currentText()
        if not target_system:
            self.add_log("错误: 请指定目标系统", "error")
            return
        
        # 禁用目标选择下拉框
        self.target_combo.setEnabled(False)
        
        # 创建入侵线程
        self.breach_thread = BreachThread(target_system, self)
        
        # 连接信号
        self.breach_thread.update_progress.connect(self.update_progress)
        self.breach_thread.update_status.connect(self.add_log)
        self.breach_thread.breach_complete.connect(self.breach_completed)
        self.breach_thread.update_data_viewer.connect(self.start_data_viewer)
        
        # 更新UI
        self.breach_button.setText("终止入侵")
        self.status_indicator.setStyleSheet(f"color: #FF0000; border: none; font-size: 14px;")
        self.status_indicator.setText("● 正在入侵")
        self.progress_bar.setValue(0)
        
        # 初始化日志
        self.clear_log()
        self.add_log(f"目标锁定: {target_system}", "info")
        self.add_log(f"初始化入侵模块...", "info")
        self.add_log(f"加载攻击向量...", "info")
        
        # 启动线程
        self.breach_thread.start()
    
    def start_data_viewer(self):
        """启动数据查看器"""
        self.hex_viewer.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def add_log(self, text, log_type="info"):
        """添加日志条目"""
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # 添加时间戳
        time_format = QTextCharFormat()
        time_format.setForeground(QBrush(QColor("#999999")))
        cursor.insertText(f"[{time.strftime('%H:%M:%S')}] ", time_format)
        
        # 根据类型设置文本颜色
        format = QTextCharFormat()
        if log_type == "info":
            format.setForeground(QBrush(QColor(TEXT_COLOR)))
        elif log_type == "warning":
            format.setForeground(QBrush(QColor("#FFAA00")))
        elif log_type == "error":
            format.setForeground(QBrush(QColor(ERROR_COLOR)))
        elif log_type == "success":
            format.setForeground(QBrush(QColor(SUCCESS_COLOR)))
        
        cursor.insertText(f"{text}\n", format)
        
        # 滚动到底部
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()
    
    def clear_log(self):
        """清除日志"""
        self.log_text.clear()
    
    def breach_completed(self, success):
        """入侵完成处理"""
        if success:
            self.status_indicator.setStyleSheet(f"color: {SUCCESS_COLOR}; border: none; font-size: 14px;")
            self.status_indicator.setText("● 入侵成功")
            self.add_log("入侵操作已成功完成", "success")
            
            # 显示额外的成功信息
            target_system = self.target_combo.currentText()
            self.add_log(f"已获取 {target_system} 的管理员权限", "success")
            
            # 添加更详细的入侵结果
            self.add_log(f"数据下载通道已建立", "info")
            self.add_log(f"后门已安装并激活", "info")
            
            # 添加后门位置和使用的入侵方法等详细信息
            if self.breach_thread:
                self.add_log("", "info")  # 空行
                self.add_log("--- 入侵详情 ---", "info")
                self.add_log(f"入侵方法: {self.breach_thread.exploit_method}", "info")
                self.add_log(f"后门路径: {self.breach_thread.backdoor_path}", "success")
                self.add_log(f"控制接口: TCP/{random.randint(10000, 65000)}", "info")
                self.add_log(f"连接加密: {random.choice(['AES-256', 'Blowfish', 'RSA-4096', 'ChaCha20'])}", "info")
                
                # 显示代理链信息
                proxy_chain = " -> ".join(self.breach_thread.proxy_servers)
                self.add_log(f"代理链路: {proxy_chain} -> 目标", "info")
                
                # 模拟权限信息
                self.add_log(f"获得权限: {random.choice(['root', 'administrator', 'system', 'SYSTEM', 'admin'])}", "success")
                
                # 随机显示一些有趣的文件路径
                self.add_log("", "info")  # 空行
                self.add_log("--- 发现敏感文件 ---", "info")
                file_paths = [
                    "/etc/shadow",
                    "/var/www/config.php",
                    "/root/.ssh/id_rsa",
                    "C:\\Windows\\System32\\config\\SAM",
                    "/home/admin/credentials.txt",
                    "C:\\Program Files\\internal\\api_keys.ini",
                    "/var/db/system.key",
                    "D:\\Backup\\financial_2023.xlsx"
                ]
                for _ in range(3):
                    self.add_log(f"发现文件: {random.choice(file_paths)}", "success")
        else:
            self.status_indicator.setStyleSheet(f"color: {ERROR_COLOR}; border: none; font-size: 14px;")
            self.status_indicator.setText("● 入侵失败")
            self.add_log("入侵操作失败", "error")
            
            # 显示失败原因
            reasons = [
                "目标系统激活了应急锁定协议",
                "检测到蜜罐，攻击被重定向",
                "身份被跟踪，连接已紧急切断",
                "防入侵系统已触发反制措施",
                "加密算法动态变换导致解密失败"
            ]
            failure_reason = random.choice(reasons)
            self.add_log(f"失败原因: {failure_reason}", "error")
            
            # 添加更详细的失败信息
            if self.breach_thread:
                self.add_log("", "error")  # 空行
                self.add_log("--- 失败详情 ---", "error")
                self.add_log(f"中断阶段: {random.choice(BREACH_PHASES)}", "error")
                self.add_log(f"尝试方法: {self.breach_thread.exploit_method}", "info")
                
                # 显示代理链信息
                if self.breach_thread.proxy_servers:
                    compromised_proxy = random.choice(self.breach_thread.proxy_servers)
                    self.add_log(f"可能暴露节点: {compromised_proxy}", "warning")
                
                # 随机安全建议
                self.add_log("", "warning")  # 空行
                self.add_log("--- 安全建议 ---", "warning")
                recommendations = [
                    "重置代理链，使用新的跳板地址",
                    "修改攻击特征，避免被特征识别",
                    "更新漏洞利用工具包到最新版本",
                    "使用时间延迟，降低检测概率",
                    "增加混淆层级，避免特征匹配"
                ]
                for _ in range(2):
                    self.add_log(f"建议: {random.choice(recommendations)}", "warning")
        
        self.breach_button.setText("开始入侵")
        self.target_combo.setEnabled(True)
        
        # 停止数据查看器的动态更新，但保留内容
        if self.hex_viewer.active:
            self.hex_viewer.active = False
            self.hex_viewer.update_timer.stop()
    
    def mousePressEvent(self, event):
        """鼠标按下事件，用于移动窗口"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，移动窗口"""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def keyPressEvent(self, event):
        """按键事件处理"""
        # Esc键关闭窗口
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止入侵线程
        if self.breach_thread and self.breach_thread.isRunning():
            self.breach_thread.stop()
            self.breach_thread.wait(1000)  # 等待最多1秒
        super().closeEvent(event) 