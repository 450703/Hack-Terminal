#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush

# 字符集，用于代码雨的显示
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=_+[]{}|;:'\",.<>/?"

class CodeRainWindow(QWidget):
    """代码雨效果窗口"""
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
        self.initUI()
        self.initRain()
        
        # 开始动画计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRain)
        self.timer.start(50)  # 每50ms更新一次
        
        # 鼠标追踪
        self.setMouseTracking(True)
        self.drag_position = None
        
        # 设置窗口位置在右上角
        self.positionWindow()
    
    def initUI(self):
        """初始化界面"""
        # 设置窗口大小 - 增大窗口尺寸
        self.resize(800, 600)
        self.setWindowTitle("Matrix Code Rain")
        
        # 设置背景色
        self.setStyleSheet("background-color: #000000;")
        
        # 设置窗口半透明
        self.setWindowOpacity(0.9)
    
    def positionWindow(self):
        """设置窗口位置在右上角"""
        desktop = QDesktopWidget().availableGeometry()
        self.move(desktop.width() - self.width() - 20, 50)
    
    def initRain(self):
        """初始化雨滴数据"""
        # 屏幕分成列，每列可能有一个雨滴
        self.char_width = 20  # 增大字符宽度
        self.char_height = 30  # 增大字符高度
        
        # 计算列数和行数
        self.columns = self.width() // self.char_width
        self.rows = self.height() // self.char_height
        
        # 雨滴位置，-1表示该列当前没有雨滴
        self.drops = [-1] * self.columns
        
        # 雨滴长度
        self.drop_length = [random.randint(5, 20) for _ in range(self.columns)]
        
        # 雨滴速度
        self.drop_speed = [random.uniform(0.3, 1.0) for _ in range(self.columns)]
        
        # 雨滴字符
        self.drop_chars = [[] for _ in range(self.columns)]
        
        # 雨滴亮度
        self.drop_brightness = [[] for _ in range(self.columns)]
        
        # 初始化一些雨滴
        for i in range(0, self.columns, 3):  # 每3列初始化一个雨滴
            self.drops[i] = random.randint(0, self.rows // 2)
            self.generateDropChars(i)
    
    def generateDropChars(self, col):
        """为一个雨滴生成随机字符"""
        length = self.drop_length[col]
        self.drop_chars[col] = [random.choice(CHARSET) for _ in range(length)]
        
        # 设置亮度，头部最亮，尾部最暗
        brightness = []
        for i in range(length):
            if i == 0:
                # 头部亮度255
                brightness.append(255)
            else:
                # 后面逐渐变暗
                b = max(0, 255 - (i * 255 // length))
                brightness.append(b)
        
        self.drop_brightness[col] = brightness
    
    def updateRain(self):
        """更新雨滴位置"""
        for i in range(self.columns):
            # 随机可能产生新雨滴
            if self.drops[i] == -1 and random.random() < 0.02:
                self.drops[i] = 0
                self.generateDropChars(i)
            
            # 更新现有雨滴位置
            if self.drops[i] >= 0:
                self.drops[i] += self.drop_speed[i]
                
                # 如果雨滴超出屏幕底部，移除它
                if self.drops[i] - self.drop_length[i] > self.rows:
                    self.drops[i] = -1
                
                # 随机改变一些字符
                if random.random() < 0.1:
                    pos = random.randint(0, self.drop_length[i] - 1)
                    if pos < len(self.drop_chars[i]):
                        self.drop_chars[i][pos] = random.choice(CHARSET)
        
        # 触发重绘
        self.update()
    
    def paintEvent(self, event):
        """绘制事件，用于显示代码雨"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 设置字体 - 增大字体
        font = QFont("Consolas", 16)  # 字体大小从12增加到16
        font.setStyleHint(QFont.Monospace)
        painter.setFont(font)
        
        for i in range(self.columns):
            if self.drops[i] >= 0:
                # 绘制雨滴中的每个字符
                for j in range(self.drop_length[i]):
                    y_pos = int((self.drops[i] - j) * self.char_height)
                    
                    # 如果字符位置在屏幕内，则绘制
                    if 0 <= y_pos < self.height() and j < len(self.drop_chars[i]):
                        # 设置颜色，根据字符位置调整亮度
                        if j < len(self.drop_brightness[i]):
                            brightness = self.drop_brightness[i][j]
                        else:
                            brightness = 100
                        
                        color = QColor(0, brightness, 0)
                        painter.setPen(color)
                        
                        # 绘制字符
                        x_pos = i * self.char_width
                        painter.drawText(QRect(x_pos, y_pos, self.char_width, self.char_height), 
                                        Qt.AlignCenter, self.drop_chars[i][j])
    
    def resizeEvent(self, event):
        """窗口大小改变时，重新计算雨滴"""
        # 重新计算列数和行数
        self.columns = self.width() // self.char_width
        self.rows = self.height() // self.char_height
        
        # 调整雨滴数组大小
        old_columns = len(self.drops)
        if self.columns > old_columns:
            # 如果列增加了，添加新列
            self.drops.extend([-1] * (self.columns - old_columns))
            self.drop_length.extend([random.randint(5, 20) for _ in range(self.columns - old_columns)])
            self.drop_speed.extend([random.uniform(0.3, 1.0) for _ in range(self.columns - old_columns)])
            self.drop_chars.extend([[] for _ in range(self.columns - old_columns)])
            self.drop_brightness.extend([[] for _ in range(self.columns - old_columns)])
        else:
            # 如果列减少了，截断数组
            self.drops = self.drops[:self.columns]
            self.drop_length = self.drop_length[:self.columns]
            self.drop_speed = self.drop_speed[:self.columns]
            self.drop_chars = self.drop_chars[:self.columns]
            self.drop_brightness = self.drop_brightness[:self.columns]
    
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
        # 停止计时器
        self.timer.stop()
        super().closeEvent(event) 