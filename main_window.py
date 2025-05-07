#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QLineEdit, 
                             QFrame, QSizePolicy, QApplication, QDesktopWidget)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal, pyqtSlot, QPoint
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush, QPen, QFontDatabase

from code_rain import CodeRainWindow
from network_scanner import NetworkScannerWindow
from system_breach import SystemBreachWindow
from threat_map import ThreatMapWindow

# 自定义标题栏样式常量
TITLE_COLOR = "#00FF00"
BG_COLOR = "#000000"
HIGHLIGHT_COLOR = "#00FFAA"
DEFAULT_FONT = "Consolas"
DEFAULT_FONT_SIZE = 14  # 增大默认字体大小

class CustomTitleBar(QWidget):
    """自定义窗口标题栏"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(35)  # 增大标题栏高度
        self.is_pressed = False
        self.start_pos = None
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 窗口标题
        self.title_label = QLabel("HACKER TERMINAL v1.0")
        self.title_label.setStyleSheet(f"color: {TITLE_COLOR}; font-weight: bold; font-family: {DEFAULT_FONT}; font-size: 16px;")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # 窗口按钮
        self.minimize_button = QPushButton("_")
        self.minimize_button.setFixedSize(35, 35)
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        
        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(35, 35)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(35, 35)
        self.close_button.clicked.connect(self.parent.close)
        
        # 设置按钮样式
        self.set_button_style()
        
        # 添加控件到布局
        layout.addSpacing(10)
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)
    
    def set_button_style(self):
        """设置按钮样式"""
        style = f"""
            QPushButton {{
                background-color: transparent;
                color: {TITLE_COLOR};
                border: none;
                font-family: {DEFAULT_FONT};
                font-weight: bold;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 255, 170, 30%);
                color: white;
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 255, 170, 50%);
            }}
        """
        
        self.minimize_button.setStyleSheet(style)
        self.maximize_button.setStyleSheet(style)
        self.close_button.setStyleSheet(style)
    
    def toggle_maximize(self):
        """切换窗口最大化状态"""
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
    
    def mousePressEvent(self, event):
        """处理鼠标按下事件，用于移动窗口"""
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self.start_pos = event.globalPos()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """处理鼠标移动事件，移动窗口"""
        if self.is_pressed:
            if self.parent.isMaximized():
                self.parent.showNormal()
            
            # 计算移动距离
            move_pos = event.globalPos() - self.start_pos
            self.start_pos = event.globalPos()
            self.parent.move(self.parent.pos() + move_pos)
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        self.is_pressed = False
        return super().mouseReleaseEvent(event)


class Terminal(QTextEdit):
    """自定义终端文本显示控件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # 打字效果计时器
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.type_next_char)
        self.typing_text = ""
        self.typing_index = 0
        self.typing_speed = 30  # 每个字符间隔时间(ms)
        
        # 光标闪烁效果
        self.cursor_visible = True
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.toggle_cursor)
        self.cursor_timer.start(500)  # 500ms闪烁一次
    
    def setup_ui(self):
        """设置界面"""
        self.setReadOnly(True)
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {BG_COLOR};
                color: {TITLE_COLOR};
                border: 1px solid {TITLE_COLOR};
                font-family: {DEFAULT_FONT};
                font-size: {DEFAULT_FONT_SIZE}px;
                selection-background-color: {HIGHLIGHT_COLOR};
                selection-color: {BG_COLOR};
            }}
        """)
        
        # 设置等宽字体
        font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
    
    def append_text(self, text):
        """添加文本，不带打字效果"""
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
    
    def type_text(self, text):
        """使用打字效果显示文本"""
        self.typing_text = text
        self.typing_index = 0
        self.typing_timer.start(self.typing_speed)
    
    def type_next_char(self):
        """打字效果，逐个字符显示"""
        if self.typing_index < len(self.typing_text):
            char = self.typing_text[self.typing_index]
            self.append_text(char)
            self.typing_index += 1
            
            # 随机延迟，使打字效果更自然
            delay = self.typing_speed
            if random.random() < 0.1:  # 10%的几率有额外延迟
                delay += random.randint(50, 200)
            self.typing_timer.setInterval(delay)
        else:
            self.typing_timer.stop()
    
    def toggle_cursor(self):
        """切换光标可见性，实现闪烁效果"""
        self.cursor_visible = not self.cursor_visible
        if self.cursor_visible:
            self.append_text("█")
            cursor = self.textCursor()
            cursor.deletePreviousChar()
            self.setTextCursor(cursor)
        else:
            self.append_text(" ")
            cursor = self.textCursor()
            cursor.deletePreviousChar()
            self.setTextCursor(cursor)


class CommandInput(QLineEdit):
    """命令输入控件"""
    
    # 自定义信号
    command_entered = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.history = []
        self.history_index = 0
    
    def setup_ui(self):
        """设置界面"""
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_COLOR};
                color: {TITLE_COLOR};
                border: 1px solid {TITLE_COLOR};
                border-radius: 0px;
                padding: 5px 8px;
                font-family: {DEFAULT_FONT};
                font-size: {DEFAULT_FONT_SIZE}px;
                selection-background-color: {HIGHLIGHT_COLOR};
                selection-color: {BG_COLOR};
                min-height: 30px;
            }}
        """)
        
        self.setPlaceholderText("输入命令...")
        
        # 设置等宽字体
        font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
    
    def keyPressEvent(self, event):
        """处理按键事件"""
        key = event.key()
        
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            command = self.text().strip()
            if command:
                self.command_entered.emit(command)
                
                # 添加到历史记录
                if not self.history or self.history[-1] != command:
                    self.history.append(command)
                self.history_index = len(self.history)
                
                # 清空输入框
                self.clear()
        
        elif key == Qt.Key_Up:
            # 浏览历史命令（向上）
            if self.history and self.history_index > 0:
                self.history_index -= 1
                self.setText(self.history[self.history_index])
        
        elif key == Qt.Key_Down:
            # 浏览历史命令（向下）
            if self.history and self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.setText(self.history[self.history_index])
            elif self.history_index == len(self.history) - 1:
                self.history_index = len(self.history)
                self.clear()
        
        else:
            super().keyPressEvent(event)


class HackerConsole(QMainWindow):
    """黑客模拟主窗口"""
    
    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint)
        self.init_ui()
        self.setup_connections()
        self.child_windows = []
        
        # 初始化模拟启动序列
        QTimer.singleShot(500, self.start_boot_sequence)
        
        self.code_rain_window = None
        self.network_scanner_window = None
        self.system_breach_window = None
        self.threat_map_window = None
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口大小和位置 - 增大窗口尺寸
        self.resize(1000, 700)
        self.center_on_screen()
        
        # 设置窗口样式
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_COLOR};
                border: 1px solid {TITLE_COLOR};
            }}
        """)
        
        # 创建中央部件和布局
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 添加自定义标题栏
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # 添加水平分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(f"background-color: {TITLE_COLOR};")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)
        
        # 终端输出区域
        self.terminal = Terminal()
        main_layout.addWidget(self.terminal, stretch=1)
        
        # 添加水平分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet(f"background-color: {TITLE_COLOR};")
        separator2.setFixedHeight(1)
        main_layout.addWidget(separator2)
        
        # 命令输入区域
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(8, 8, 8, 8)
        
        prompt_label = QLabel("> ")
        prompt_label.setStyleSheet(f"color: {TITLE_COLOR}; font-weight: bold; font-family: {DEFAULT_FONT}; font-size: {DEFAULT_FONT_SIZE}px;")
        input_layout.addWidget(prompt_label)
        
        self.command_input = CommandInput()
        input_layout.addWidget(self.command_input)
        
        main_layout.addLayout(input_layout)
        
        # 设置中央部件
        self.setCentralWidget(central_widget)
    
    def center_on_screen(self):
        """将窗口居中显示"""
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def setup_connections(self):
        """设置信号连接"""
        self.command_input.command_entered.connect(self.process_command)
    
    def start_boot_sequence(self):
        """启动序列，显示启动文本"""
        boot_sequence = [
            "正在初始化系统...",
            "正在加载核心组件...",
            "检查安全协议...",
            "初始化网络接口...",
            "正在连接到隐藏服务器...",
            "加载黑客工具集...",
            "覆盖安全追踪...",
            "加载完成. 系统就绪.\n",
            "\n欢迎使用黑客终端系统 v1.0\n",
            "输入 'help' 查看可用命令.\n"
        ]
        
        delay = 0
        for line in boot_sequence:
            # 逐行显示，每行有延迟
            QTimer.singleShot(delay, lambda text=line: self.terminal.type_text(text))
            delay += len(line) * 40 + 500
    
    def process_command(self, command):
        """处理输入的命令"""
        self.terminal.type_text(f"\n> {command}\n")
        
        command = command.lower()
        
        if command == "help":
            self.show_help()
        elif command == "clear" or command == "cls":
            self.terminal.clear()
        elif command == "exit" or command == "quit":
            self.close()
        elif command == "matrix" or command == "code":
            self.show_code_rain()
        elif command == "scan" or command == "nmap":
            self.show_network_scanner()
        elif command == "hack" or command == "breach":
            self.show_system_breach()
        elif command == "map" or command == "threatmap":
            self.show_threat_map()
        else:
            self.terminal.type_text(f"未知命令: {command}\n")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
可用命令列表:
  help      - 显示此帮助信息
  clear/cls - 清空终端
  exit/quit - 退出程序
  matrix    - 显示代码雨效果
  scan      - 显示网络扫描窗口
  hack      - 显示系统入侵窗口
  map       - 启动全球网络威胁地图
        
"""
        self.terminal.type_text(help_text)
    
    def show_code_rain(self):
        """显示代码雨窗口"""
        self.terminal.type_text("正在启动矩阵代码雨...\n")
        code_rain = CodeRainWindow(self)
        code_rain.show()
        self.child_windows.append(code_rain)
    
    def show_network_scanner(self):
        """显示网络扫描窗口"""
        self.terminal.type_text("正在启动网络扫描模块...\n")
        scanner = NetworkScannerWindow(self)
        scanner.show()
        self.child_windows.append(scanner)
    
    def show_system_breach(self):
        """显示系统入侵窗口"""
        self.terminal.type_text("正在启动系统入侵模块...\n")
        breach = SystemBreachWindow(self)
        breach.show()
        self.child_windows.append(breach)
    
    def show_threat_map(self):
        """显示网络威胁地图窗口"""
        self.terminal.type_text("正在启动全球网络威胁地图...\n")
        
        if not self.threat_map_window:
            self.threat_map_window = ThreatMapWindow()
            # 设置关闭信号
            self.threat_map_window.closed.connect(self.on_threat_map_closed)
        
        self.threat_map_window.show()
        self.terminal.type_text("威胁地图已启动，显示全球实时网络攻击")
    
    def on_threat_map_closed(self):
        """处理威胁地图窗口关闭事件"""
        self.threat_map_window = None
        self.terminal.type_text("威胁地图已关闭")
    
    def closeEvent(self, event):
        """窗口关闭时关闭所有子窗口"""
        for window in self.child_windows:
            try:
                window.close()
            except:
                pass
        
        # 确保关闭威胁地图窗口
        if self.threat_map_window:
            try:
                self.threat_map_window.close()
            except:
                pass
        
        super().closeEvent(event) 