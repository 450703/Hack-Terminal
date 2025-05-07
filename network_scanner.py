#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTreeWidget, QTreeWidgetItem, QProgressBar, 
                            QPushButton, QFrame, QDesktopWidget, QLineEdit,
                            QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QBrush

# 样式常量
BG_COLOR = "#000000"
TEXT_COLOR = "#00FF00"
ACCENT_COLOR = "#00FFAA"
HIGHLIGHT_COLOR = "#FF0000"
DEFAULT_FONT = "Consolas"
DEFAULT_FONT_SIZE = 14  # 增大默认字体大小

# 模拟网络服务
COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy"
}

# 模拟漏洞
VULNERABILITIES = [
    "Default Credentials",
    "SQL Injection",
    "XSS Vulnerability",
    "Remote Code Execution",
    "Directory Traversal",
    "Authentication Bypass",
    "Outdated Software",
    "Weak Encryption",
    "Information Disclosure",
    "Open Port"
]

class ScannerThread(QThread):
    """用于在后台执行扫描操作的线程"""
    
    # 自定义信号
    progress_updated = pyqtSignal(int)
    host_found = pyqtSignal(str, str, str)  # IP, 描述, 类型(info/warning/critical)
    port_found = pyqtSignal(str, int, str, str)  # IP, 端口, 服务名, 类型
    scan_complete = pyqtSignal()
    
    def __init__(self, ip_range, port_range, parent=None):
        super().__init__(parent)
        self.ip_range = ip_range
        self.port_range = port_range
        self.is_running = True
    
    def stop(self):
        """停止扫描"""
        self.is_running = False
    
    def run(self):
        """执行扫描操作"""
        total_ips = 10  # 模拟扫描的IP数量
        current_progress = 0
        
        # 生成目标IP，严格基于用户输入的IP范围
        target_ips = []
        
        # 定义处理IP生成的函数
        def generate_ips_for_partial(parts, count=total_ips):
            """根据部分IP生成完整IP地址"""
            result = []
            if len(parts) == 1:  # 如 "192"
                for _ in range(count):
                    ip = f"{parts[0]}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
                    result.append(ip)
            elif len(parts) == 2:  # 如 "192.1"
                for _ in range(count):
                    ip = f"{parts[0]}.{parts[1]}.{random.randint(0, 255)}.{random.randint(1, 254)}"
                    result.append(ip)
            elif len(parts) == 3:  # 如 "192.168.1"
                for _ in range(count):
                    ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{random.randint(1, 254)}"
                    result.append(ip)
            else:  # 无效部分
                for _ in range(count):
                    ip = f"192.168.1.{random.randint(1, 254)}"
                    result.append(ip)
            return result
        
        if self.ip_range:
            # 处理输入，去除可能的空格
            ip_range = self.ip_range.strip()
            
            # 处理CIDR格式 (例如 192.168.1.0/24)
            if '/' in ip_range:
                ip_base = ip_range.split('/')[0].strip()
            else:
                ip_base = ip_range
            
            # 解析IP部分，支持部分IP格式（如"192.1"）
            parts = [p for p in ip_base.split('.') if p]  # 移除空部分
            
            # 处理特殊情况: "192.1"这样的格式会生成两个部分
            if len(parts) == 2:
                # 专门处理"192.1"格式，确保生成"192.1.x.y"而不是默认的"192.168.1.x"
                for _ in range(total_ips):
                    third = random.randint(0, 255)
                    fourth = random.randint(1, 254)
                    ip = f"{parts[0]}.{parts[1]}.{third}.{fourth}"
                    target_ips.append(ip)
            elif len(parts) == 1:
                # 单段IP，如"192"
                for _ in range(total_ips):
                    second = random.randint(0, 255)
                    third = random.randint(0, 255)
                    fourth = random.randint(1, 254)
                    ip = f"{parts[0]}.{second}.{third}.{fourth}"
                    target_ips.append(ip)
            elif len(parts) == 3:
                # 3段IP，如"192.168.1"
                for _ in range(total_ips):
                    fourth = random.randint(1, 254)
                    ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{fourth}"
                    target_ips.append(ip)
            elif len(parts) == 4:
                # 完整IP
                try:
                    last_part = int(parts[3])
                    if last_part == 0:  # 网段，如"192.168.1.0"
                        for _ in range(total_ips):
                            fourth = random.randint(1, 254)
                            ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{fourth}"
                            target_ips.append(ip)
                    else:  # 具体IP，生成附近IP
                        base = max(1, last_part - 5)
                        for i in range(total_ips):
                            if base + i > 254:
                                ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{base - (i - (254-base))}"
                            else:
                                ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{base + i}"
                            target_ips.append(ip)
                except ValueError:
                    # 最后一段不是数字
                    for _ in range(total_ips):
                        fourth = random.randint(1, 254)
                        ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{fourth}"
                        target_ips.append(ip)
            else:
                # 无效格式，使用默认
                target_ips = generate_ips_for_partial([], total_ips)
        else:
            # 未提供IP范围，使用默认值
            for _ in range(total_ips):
                ip = f"192.168.1.{random.randint(1, 254)}"
                target_ips.append(ip)
        
        # 确保没有重复的IP
        target_ips = list(dict.fromkeys(target_ips))
        
        # 如果生成的IP不足，补充到需要的数量
        while len(target_ips) < total_ips:
            if len(parts) >= 1:
                # 使用现有IP部分生成新IP
                new_ips = generate_ips_for_partial(parts, total_ips - len(target_ips))
                for ip in new_ips:
                    if ip not in target_ips:
                        target_ips.append(ip)
                        if len(target_ips) >= total_ips:
                            break
            else:
                # 使用默认值
                ip = f"192.168.1.{random.randint(1, 254)}"
                if ip not in target_ips:
                    target_ips.append(ip)
        
        # 解析端口范围
        port_list = []
        if self.port_range:
            try:
                # 尝试解析用户输入的端口范围，例如："1-1024"或"80,443,8080"
                if '-' in self.port_range:
                    port_parts = self.port_range.split('-')
                    if len(port_parts) == 2:
                        start_port = max(1, min(65535, int(port_parts[0])))
                        end_port = max(1, min(65535, int(port_parts[1])))
                        
                        if start_port > end_port:
                            start_port, end_port = end_port, start_port
                        
                        # 从预定义服务中选择在范围内的
                        common_ports = [p for p in COMMON_SERVICES.keys() if start_port <= p <= end_port]
                        
                        # 至少选择5个端口，如果预定义服务中没有足够的端口，添加一些随机端口
                        if len(common_ports) < 5:
                            needed = 5 - len(common_ports)
                            # 避免重复
                            extra_ports = []
                            while len(extra_ports) < needed and len(extra_ports) < (end_port - start_port + 1 - len(common_ports)):
                                p = random.randint(start_port, end_port)
                                if p not in common_ports and p not in extra_ports:
                                    extra_ports.append(p)
                            
                            port_list = common_ports + extra_ports
                        else:
                            # 随机选择最多8个常用端口
                            port_list = random.sample(common_ports, min(8, len(common_ports)))
                elif ',' in self.port_range:
                    # 处理逗号分隔的端口列表
                    try:
                        port_parts = self.port_range.split(',')
                        for part in port_parts:
                            port = int(part.strip())
                            if 1 <= port <= 65535 and port not in port_list:
                                port_list.append(port)
                    except:
                        pass
                else:
                    # 可能是单个端口
                    try:
                        port = int(self.port_range.strip())
                        if 1 <= port <= 65535:
                            port_list = [port]
                    except:
                        pass
            except:
                # 解析失败，使用默认端口列表
                port_list = random.sample(list(COMMON_SERVICES.keys()), min(8, len(COMMON_SERVICES)))
        
        # 如果端口列表仍然为空，使用默认端口
        if not port_list:
            port_list = random.sample(list(COMMON_SERVICES.keys()), min(8, len(COMMON_SERVICES)))
        
        # 开始扫描过程
        for ip_index, ip in enumerate(target_ips):
            if not self.is_running:
                break
            
            # 通知发现主机
            status_type = random.choice(["info", "warning", "critical"])
            desc = f"Host is up ({random.randint(1, 100)}ms latency)"
            self.host_found.emit(ip, desc, status_type)
            
            # 为每个IP扫描端口
            ports_scanned = 0
            for port in port_list:
                if not self.is_running:
                    break
                
                # 随机决定端口是否开放 (70%几率开放)
                if random.random() < 0.7:
                    # 获取服务名称，如果不在预定义服务列表中，则显示"Unknown"
                    service = COMMON_SERVICES.get(port, "Unknown")
                    
                    # 80%的几率是信息，15%的几率是警告，5%的几率是严重
                    r = random.random()
                    if r < 0.8:
                        status_type = "info"
                        detail = "Open Port"
                    elif r < 0.95:
                        status_type = "warning"
                        detail = random.choice(VULNERABILITIES)
                    else:
                        status_type = "critical"
                        detail = f"Critical: {random.choice(VULNERABILITIES)}"
                    
                    # 通知发现端口
                    self.port_found.emit(ip, port, service, status_type)
                    ports_scanned += 1
                
                # 更新进度 - 每个IP的进度贡献为总进度的1/total_ips
                ip_progress = (ip_index / total_ips) * 100
                # 每个端口的扫描贡献为单个IP进度的1/len(port_list)
                port_progress = (ports_scanned / len(port_list)) * (100 / total_ips)
                current_progress = ip_progress + port_progress
                
                self.progress_updated.emit(min(int(current_progress), 99))  # 保留最后1%给完成信号
                
                # 模拟扫描延迟
                if self.is_running:
                    time.sleep(random.uniform(0.1, 0.3))
        
        # 完成扫描
        if self.is_running:
            self.progress_updated.emit(100)
            self.scan_complete.emit()


class NetworkScannerWindow(QWidget):
    """网络扫描模拟窗口"""
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
        self.initUI()
        self.scanner_thread = None
        self.drag_position = None
        
        # 设置窗口位置在右下角
        self.positionWindow()
    
    def initUI(self):
        """初始化界面"""
        # 设置窗口大小和标题 - 增大尺寸
        self.resize(900, 650)
        self.setWindowTitle("Network Scanner")
        
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
                min-height: 20px;
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
            QTreeWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                alternate-background-color: #0A0A0A;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QTreeWidget::item:selected {{
                background-color: rgba(0, 255, 170, 30%);
            }}
            QTreeWidget::item {{
                border-bottom: 1px solid #222222;
                padding: 2px;
            }}
            QHeaderView::section {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                padding: 6px;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QLineEdit {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                padding: 5px;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QGroupBox {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {TEXT_COLOR};
                margin-top: 12px;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
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
        
        title_label = QLabel("NETWORK SCANNER v1.0")
        title_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold; font-size: 16px;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
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
        
        # 目标设置区域
        target_group = QGroupBox("扫描配置")
        target_group.setMaximumHeight(120)
        target_layout = QFormLayout(target_group)
        target_layout.setContentsMargins(10, 25, 10, 10)
        
        # IP范围输入
        self.ip_range_input = QLineEdit("192.168.1.0/24")
        self.ip_range_input.setPlaceholderText("例如: 192.168.1.0/24")
        target_layout.addRow("目标IP范围:", self.ip_range_input)
        
        # 端口范围输入
        self.port_range_input = QLineEdit("1-1024")
        self.port_range_input.setPlaceholderText("例如: 1-1024")
        target_layout.addRow("端口范围:", self.port_range_input)
        
        main_layout.addWidget(target_group)
        
        # 状态布局
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("等待开始扫描...")
        self.status_label.setStyleSheet(f"font-size: {DEFAULT_FONT_SIZE}px;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(status_layout)
        
        # 结果树形视图
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["目标", "端口/服务", "状态", "详情"])
        self.results_tree.setAlternatingRowColors(True)
        self.results_tree.setColumnWidth(0, 180)
        self.results_tree.setColumnWidth(1, 180)
        self.results_tree.setColumnWidth(2, 100)
        
        # 设置字体
        tree_font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        self.results_tree.setFont(tree_font)
        
        main_layout.addWidget(self.results_tree)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.scan_button = QPushButton("开始扫描")
        self.scan_button.clicked.connect(self.toggle_scan)
        button_layout.addWidget(self.scan_button)
        
        self.clear_button = QPushButton("清除结果")
        self.clear_button.clicked.connect(self.clear_results)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # 设置布局
        self.setLayout(main_layout)
        
        # 鼠标追踪
        self.setMouseTracking(True)
    
    def positionWindow(self):
        """设置窗口位置在右下角"""
        desktop = QDesktopWidget().availableGeometry()
        self.move(desktop.width() - self.width() - 20, desktop.height() - self.height() - 40)
    
    def toggle_scan(self):
        """切换扫描状态"""
        if self.scanner_thread and self.scanner_thread.isRunning():
            # 停止扫描
            self.scanner_thread.stop()
            self.scan_button.setText("开始扫描")
            self.status_label.setText("扫描已停止")
            self.ip_range_input.setEnabled(True)
            self.port_range_input.setEnabled(True)
        else:
            # 开始扫描
            self.start_scan()
    
    def start_scan(self):
        """开始扫描操作"""
        # 获取用户输入的IP和端口范围
        ip_range = self.ip_range_input.text().strip()
        port_range = self.port_range_input.text().strip()
        
        # 输入验证 (简化版)
        if not ip_range:
            self.status_label.setText("请输入有效的IP范围")
            return
        
        # 禁用输入控件
        self.ip_range_input.setEnabled(False)
        self.port_range_input.setEnabled(False)
        
        # 创建扫描线程
        self.scanner_thread = ScannerThread(ip_range, port_range, self)
        
        # 连接信号
        self.scanner_thread.progress_updated.connect(self.update_progress)
        self.scanner_thread.host_found.connect(self.add_host)
        self.scanner_thread.port_found.connect(self.add_port)
        self.scanner_thread.scan_complete.connect(self.scan_completed)
        
        # 更新UI
        self.scan_button.setText("停止扫描")
        self.status_label.setText(f"正在扫描 {ip_range} 上的端口 {port_range}...")
        self.progress_bar.setValue(0)
        
        # 启动线程
        self.scanner_thread.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def add_host(self, ip, desc, status_type):
        """添加主机到结果树"""
        host_item = QTreeWidgetItem(self.results_tree)
        host_item.setText(0, ip)
        host_item.setText(1, "")
        host_item.setText(2, self.get_status_text(status_type))
        host_item.setText(3, desc)
        
        # 设置颜色
        for i in range(4):
            host_item.setForeground(i, QBrush(self.get_status_color(status_type)))
        
        # 展开项目
        self.results_tree.expandItem(host_item)
    
    def add_port(self, ip, port, service, status_type):
        """添加端口到结果树"""
        # 查找对应的主机项
        host_item = None
        for i in range(self.results_tree.topLevelItemCount()):
            item = self.results_tree.topLevelItem(i)
            if item.text(0) == ip:
                host_item = item
                break
        
        if not host_item:
            return
        
        # 创建端口项
        port_item = QTreeWidgetItem(host_item)
        port_item.setText(0, "")
        port_item.setText(1, f"{port}/{service}")
        port_item.setText(2, self.get_status_text(status_type))
        
        # 根据状态类型选择详情内容
        if status_type == "warning":
            vuln = random.choice(VULNERABILITIES)
            port_item.setText(3, vuln)
        elif status_type == "critical":
            vuln = random.choice(VULNERABILITIES)
            port_item.setText(3, f"Critical: {vuln}")
        else:
            port_item.setText(3, "Open Port")
        
        # 设置颜色
        for i in range(4):
            port_item.setForeground(i, QBrush(self.get_status_color(status_type)))
        
        # 滚动到最新项
        self.results_tree.scrollToItem(port_item)
    
    def get_status_text(self, status_type):
        """根据状态类型获取状态文本"""
        if status_type == "info":
            return "信息"
        elif status_type == "warning":
            return "警告"
        elif status_type == "critical":
            return "严重"
        return ""
    
    def get_status_color(self, status_type):
        """根据状态类型获取颜色"""
        if status_type == "info":
            return QColor(TEXT_COLOR)
        elif status_type == "warning":
            return QColor("#FFAA00")
        elif status_type == "critical":
            return QColor(HIGHLIGHT_COLOR)
        return QColor(TEXT_COLOR)
    
    def scan_completed(self):
        """扫描完成的处理"""
        self.status_label.setText("扫描完成")
        self.scan_button.setText("开始扫描")
        self.ip_range_input.setEnabled(True)
        self.port_range_input.setEnabled(True)
    
    def clear_results(self):
        """清除扫描结果"""
        self.results_tree.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("等待开始扫描...")
    
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
        # 停止扫描线程
        if self.scanner_thread and self.scanner_thread.isRunning():
            self.scanner_thread.stop()
            self.scanner_thread.wait(1000)  # 等待最多1秒
        super().closeEvent(event) 