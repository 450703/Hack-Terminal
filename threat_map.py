#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import math
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QDesktopWidget, QPushButton, QApplication)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QPointF, QRectF
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QBrush, QPainterPath, QLinearGradient
import sys

# 风格常量 - 与主窗口保持一致
TITLE_COLOR = "#00FF00"
BG_COLOR = "#000000"
ACCENT_COLOR = "#00FFAA"
HIGHLIGHT_COLOR = "#FF0000"
DEFAULT_FONT = "Consolas"
DEFAULT_FONT_SIZE = 14

# 模拟世界地图坐标
# 格式: "国家": (x坐标百分比, y坐标百分比)
WORLD_LOCATIONS = {
    "美国": (0.2, 0.35),
    "中国": (0.75, 0.38),
    "俄罗斯": (0.65, 0.25),
    "巴西": (0.3, 0.6),
    "印度": (0.68, 0.45),
    "日本": (0.83, 0.35),
    "德国": (0.5, 0.28),
    "法国": (0.47, 0.3),
    "英国": (0.45, 0.25),
    "澳大利亚": (0.85, 0.65),
    "加拿大": (0.22, 0.25),
    "墨西哥": (0.18, 0.45),
    "南非": (0.55, 0.65),
    "埃及": (0.55, 0.42),
    "阿根廷": (0.3, 0.7),
    "印尼": (0.8, 0.55),
    "韩国": (0.82, 0.33),
    "伊朗": (0.62, 0.4),
    "土耳其": (0.58, 0.35),
    "意大利": (0.52, 0.32),
    "西班牙": (0.45, 0.33),
    "荷兰": (0.48, 0.26),
    "瑞典": (0.5, 0.2),
    "挪威": (0.5, 0.18),
    "芬兰": (0.53, 0.18),
    "波兰": (0.53, 0.27),
    "沙特阿拉伯": (0.6, 0.42),
    "阿联酋": (0.63, 0.43),
    "泰国": (0.77, 0.48),
    "越南": (0.78, 0.5),
    "马来西亚": (0.77, 0.52),
    "新加坡": (0.77, 0.53),
    "菲律宾": (0.83, 0.5),
    "新西兰": (0.9, 0.7)
}

# 攻击类型
ATTACK_TYPES = [
    "DDoS攻击",
    "暴力破解",
    "SQL注入",
    "钓鱼攻击",
    "恶意软件",
    "勒索软件",
    "漏洞利用",
    "社会工程学",
    "APT攻击",
    "零日漏洞",
    "跨站脚本",
    "会话劫持",
    "DNS劫持",
    "数据泄露"
]

class CustomTitleBar(QWidget):
    """自定义窗口标题栏 - 与主窗口一致"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(35)  # 与主窗口一致
        self.is_pressed = False
        self.start_pos = None
        
        # 创建布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 窗口标题
        self.title_label = QLabel("实时网络威胁地图")
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
            self.maximize_button.setText("□")
        else:
            self.parent.showMaximized()
            self.maximize_button.setText("◱")
    
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
                self.maximize_button.setText("□")
            
            # 计算移动距离
            move_pos = event.globalPos() - self.start_pos
            self.start_pos = event.globalPos()
            self.parent.move(self.parent.pos() + move_pos)
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        self.is_pressed = False
        return super().mouseReleaseEvent(event)

class AttackAnimation:
    """表示一次攻击动画"""
    
    def __init__(self, source, target, map_width, map_height, attack_type=None):
        self.source = source  # 源坐标 (x, y)
        self.target = target  # 目标坐标 (x, y)
        self.progress = 0.0   # 动画进度 (0.0 ~ 1.0)
        self.speed = random.uniform(0.005, 0.02)  # 速度
        self.size = random.uniform(3, 6)          # 粒子大小
        self.active = True    # 是否活跃
        self.color = self.get_attack_color()      # 攻击颜色
        self.attack_type = attack_type or random.choice(ATTACK_TYPES)
        
        # 生成一条稍微弯曲的路径
        cx = (source[0] + target[0]) / 2
        cy = (source[1] + target[1]) / 2
        # 添加随机弯曲
        offset = random.uniform(-0.1, 0.1) * map_height
        cx += offset
        cy += offset
        
        self.control_point = (cx, cy)
    
    def update(self):
        """更新动画进度"""
        if not self.active:
            return False
            
        self.progress += self.speed
        if self.progress >= 1.0:
            self.active = False
            return False
        return True
    
    def get_current_position(self):
        """获取当前位置（贝塞尔曲线）"""
        t = self.progress
        # 二次贝塞尔曲线
        x = (1-t)**2 * self.source[0] + 2*(1-t)*t * self.control_point[0] + t**2 * self.target[0]
        y = (1-t)**2 * self.source[1] + 2*(1-t)*t * self.control_point[1] + t**2 * self.target[1]
        return (x, y)
    
    def get_attack_color(self):
        """根据攻击类型获取颜色"""
        r = random.random()
        if r < 0.3:  # 30%几率为绿色（低危）
            return QColor(0, 255, 0, 200)
        elif r < 0.7:  # 40%几率为黄色（中危）
            return QColor(255, 255, 0, 200)
        else:  # 30%几率为红色（高危）
            return QColor(255, 0, 0, 200)

class ThreatMapThread(QThread):
    """生成攻击数据的后台线程"""
    
    # 自定义信号
    new_attack = pyqtSignal(object)  # 发送一个AttackAnimation对象
    update_stats = pyqtSignal(dict)  # 更新统计信息
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_running = True
        self.map_width = 0
        self.map_height = 0
        
        # 统计数据
        self.stats = {
            "total_attacks": 0,
            "attacks_by_country": {},
            "attack_types": {}
        }
    
    def set_map_size(self, width, height):
        """设置地图尺寸"""
        self.map_width = width
        self.map_height = height
    
    def stop(self):
        """停止线程"""
        self.is_running = False
    
    def run(self):
        """运行线程"""
        countries = list(WORLD_LOCATIONS.keys())
        
        while self.is_running:
            # 随机选择源和目标国家
            source_country = random.choice(countries)
            target_country = random.choice(countries)
            
            # 确保源和目标不同
            while source_country == target_country:
                target_country = random.choice(countries)
            
            # 获取坐标并转换为实际像素坐标
            source_loc = WORLD_LOCATIONS[source_country]
            target_loc = WORLD_LOCATIONS[target_country]
            
            source_x = source_loc[0] * self.map_width
            source_y = source_loc[1] * self.map_height
            target_x = target_loc[0] * self.map_width
            target_y = target_loc[1] * self.map_height
            
            # 随机选择攻击类型
            attack_type = random.choice(ATTACK_TYPES)
            
            # 创建攻击动画
            attack = AttackAnimation(
                (source_x, source_y),
                (target_x, target_y),
                self.map_width,
                self.map_height,
                attack_type
            )
            
            # 更新统计数据
            self.stats["total_attacks"] += 1
            
            # 按国家统计
            if source_country not in self.stats["attacks_by_country"]:
                self.stats["attacks_by_country"][source_country] = 0
            self.stats["attacks_by_country"][source_country] += 1
            
            # 按攻击类型统计
            if attack_type not in self.stats["attack_types"]:
                self.stats["attack_types"][attack_type] = 0
            self.stats["attack_types"][attack_type] += 1
            
            # 发送新攻击信号
            self.new_attack.emit(attack)
            
            # 每50次攻击更新一次统计数据
            if self.stats["total_attacks"] % 50 == 0:
                self.update_stats.emit(self.stats.copy())
            
            # 随机延迟，控制攻击生成频率
            time.sleep(random.uniform(0.1, 1.0))

class ThreatMapWindow(QWidget):
    """卡巴斯基风格网络威胁地图窗口"""
    
    # 添加关闭信号
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)  # 无边框窗口
        self.initUI()
        
        # 攻击动画列表
        self.active_attacks = []
        
        # 动画定时器
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(16)  # ~60 FPS
        
        # 数据生成线程
        self.threat_thread = ThreatMapThread(self)
        self.threat_thread.new_attack.connect(self.add_attack)
        self.threat_thread.update_stats.connect(self.update_statistics)
        
        # 拖动相关
        self.drag_position = None
        
        # 窗口位置设置
        self.positionWindow()
        
        # 基本统计数据
        self.attack_stats = {
            "total_attacks": 0,
            "attacks_by_country": {},
            "attack_types": {}
        }
        
        # 当前选中的攻击（用于显示详细信息）
        self.selected_attack = None
        
        # 在窗口调整大小后启动线程
        QTimer.singleShot(100, self.start_thread)
    
    def start_thread(self):
        """启动威胁数据线程"""
        # 设置地图大小
        self.threat_thread.set_map_size(self.width(), self.height())
        # 启动线程
        self.threat_thread.start()
    
    def initUI(self):
        """初始化界面"""
        # 设置窗口大小
        self.resize(1000, 700)
        self.setWindowTitle("网络威胁实时地图")
        
        # 设置窗口样式 - 与主窗口一致的边框
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TITLE_COLOR};
                font-family: {DEFAULT_FONT};
                border: 1px solid {TITLE_COLOR};
            }}
            QLabel {{
                border: none;
                font-size: {DEFAULT_FONT_SIZE}px;
            }}
        """)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
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
        
        # 创建信息面板
        self.info_panel = QWidget()
        self.info_panel.setFixedHeight(80)
        self.info_panel.setStyleSheet(f"""
            background-color: {BG_COLOR};
            border: none;
            border-bottom: 1px solid {TITLE_COLOR};
        """)
        info_layout = QHBoxLayout(self.info_panel)
        info_layout.setContentsMargins(10, 5, 10, 5)
        
        # 总攻击计数
        stats_layout = QVBoxLayout()
        self.total_attacks_label = QLabel("总攻击次数: 0")
        self.total_attacks_label.setStyleSheet(f"color: {TITLE_COLOR}; font-size: 16px; border: none;")
        stats_layout.addWidget(self.total_attacks_label)
        
        # 活跃攻击数量
        self.active_attacks_label = QLabel("活跃攻击: 0")
        self.active_attacks_label.setStyleSheet(f"color: {TITLE_COLOR}; border: none;")
        stats_layout.addWidget(self.active_attacks_label)
        
        # 当前选中的攻击信息
        self.selected_attack_label = QLabel("选择攻击以查看详情")
        self.selected_attack_label.setStyleSheet(f"color: {ACCENT_COLOR}; border: none;")
        stats_layout.addWidget(self.selected_attack_label)
        
        info_layout.addLayout(stats_layout)
        info_layout.addStretch()
        
        # 添加信息面板到主布局
        main_layout.addWidget(self.info_panel)
        
        # 添加主要地图区域（由paintEvent处理）
        self.map_area = QWidget()
        self.map_area.setStyleSheet("background-color: transparent; border: none;")
        main_layout.addWidget(self.map_area, 1)  # 1是伸展因子
        
        # 添加水平分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet(f"background-color: {TITLE_COLOR};")
        separator2.setFixedHeight(1)
        main_layout.addWidget(separator2)
        
        # 状态栏
        status_bar = QWidget()
        status_bar.setFixedHeight(25)
        status_bar.setStyleSheet(f"""
            background-color: {BG_COLOR};
            border: none;
        """)
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 10, 0)
        
        # 状态信息
        status_label = QLabel("注: 此地图模拟全球网络攻击流量，仅作为视觉效果展示")
        status_label.setStyleSheet(f"""
            color: {TITLE_COLOR};
            font-family: {DEFAULT_FONT};
            font-size: 10px;
            border: none;
        """)
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        
        # 添加状态栏到主布局
        main_layout.addWidget(status_bar)
        
        # 配置窗口
        self.setLayout(main_layout)
        
        # 启用鼠标追踪
        self.setMouseTracking(True)
    
    def positionWindow(self):
        """设置窗口位置在屏幕中央"""
        desktop = QDesktopWidget().availableGeometry()
        size = self.size()
        self.move((desktop.width() - size.width()) // 2, 
                 (desktop.height() - size.height()) // 2)
    
    def add_attack(self, attack):
        """添加新的攻击动画"""
        self.active_attacks.append(attack)
    
    def update_animations(self):
        """更新所有攻击动画"""
        # 更新动画状态
        self.active_attacks = [attack for attack in self.active_attacks if attack.update()]
        
        # 更新活跃攻击标签
        self.active_attacks_label.setText(f"活跃攻击: {len(self.active_attacks)}")
        
        # 触发重绘
        self.update()
    
    def update_statistics(self, stats):
        """更新统计数据"""
        self.attack_stats = stats
        self.total_attacks_label.setText(f"总攻击次数: {stats['total_attacks']}")
    
    def paintEvent(self, event):
        """绘制地图和攻击动画"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        self.draw_background(painter)
        
        # 绘制地图轮廓
        self.draw_map_outline(painter)
        
        # 绘制节点
        self.draw_locations(painter)
        
        # 绘制攻击
        self.draw_attacks(painter)
    
    def draw_background(self, painter):
        """绘制背景"""
        # 创建渐变色背景
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 10, 30))  # 稍微调亮，更符合黑客风格
        gradient.setColorAt(1, QColor(0, 5, 15))
        
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # 绘制网格线
        grid_spacing = 40
        painter.setPen(QPen(QColor(0, 120, 0, 30), 1))
        
        # 绘制垂直网格线
        for x in range(0, self.width(), grid_spacing):
            painter.drawLine(x, 0, x, self.height())
        
        # 绘制水平网格线
        for y in range(0, self.height(), grid_spacing):
            painter.drawLine(0, y, self.width(), y)
    
    def draw_map_outline(self, painter):
        """绘制简化的世界地图轮廓"""
        # 设置画笔
        painter.setPen(QPen(QColor(0, 150, 0, 100), 1))  # 使线条更明显
        
        # 此处使用简化的世界地图轮廓，仅作为示意
        # 北美大致轮廓
        north_america = QPainterPath()
        north_america.moveTo(0.15 * self.width(), 0.2 * self.height())
        north_america.lineTo(0.25 * self.width(), 0.25 * self.height())
        north_america.lineTo(0.28 * self.width(), 0.35 * self.height())
        north_america.lineTo(0.22 * self.width(), 0.4 * self.height())
        north_america.lineTo(0.18 * self.width(), 0.48 * self.height())
        north_america.lineTo(0.12 * self.width(), 0.42 * self.height())
        north_america.lineTo(0.1 * self.width(), 0.3 * self.height())
        north_america.closeSubpath()
        painter.drawPath(north_america)
        
        # 南美大致轮廓
        south_america = QPainterPath()
        south_america.moveTo(0.22 * self.width(), 0.5 * self.height())
        south_america.lineTo(0.28 * self.width(), 0.55 * self.height())
        south_america.lineTo(0.25 * self.width(), 0.7 * self.height())
        south_america.lineTo(0.20 * self.width(), 0.8 * self.height())
        south_america.lineTo(0.18 * self.width(), 0.6 * self.height())
        south_america.closeSubpath()
        painter.drawPath(south_america)
        
        # 欧洲大致轮廓
        europe = QPainterPath()
        europe.moveTo(0.45 * self.width(), 0.2 * self.height())
        europe.lineTo(0.55 * self.width(), 0.22 * self.height())
        europe.lineTo(0.53 * self.width(), 0.35 * self.height())
        europe.lineTo(0.45 * self.width(), 0.38 * self.height())
        europe.lineTo(0.42 * self.width(), 0.28 * self.height())
        europe.closeSubpath()
        painter.drawPath(europe)
        
        # 非洲大致轮廓
        africa = QPainterPath()
        africa.moveTo(0.45 * self.width(), 0.38 * self.height())
        africa.lineTo(0.55 * self.width(), 0.35 * self.height())
        africa.lineTo(0.58 * self.width(), 0.45 * self.height())
        africa.lineTo(0.55 * self.width(), 0.6 * self.height())
        africa.lineTo(0.45 * self.width(), 0.65 * self.height())
        africa.lineTo(0.4 * self.width(), 0.55 * self.height())
        africa.lineTo(0.42 * self.width(), 0.4 * self.height())
        africa.closeSubpath()
        painter.drawPath(africa)
        
        # 亚洲大致轮廓
        asia = QPainterPath()
        asia.moveTo(0.55 * self.width(), 0.22 * self.height())
        asia.lineTo(0.8 * self.width(), 0.25 * self.height())
        asia.lineTo(0.85 * self.width(), 0.35 * self.height())
        asia.lineTo(0.75 * self.width(), 0.45 * self.height())
        asia.lineTo(0.67 * self.width(), 0.5 * self.height())
        asia.lineTo(0.58 * self.width(), 0.45 * self.height())
        asia.lineTo(0.55 * self.width(), 0.35 * self.height())
        asia.closeSubpath()
        painter.drawPath(asia)
        
        # 澳大利亚大致轮廓
        australia = QPainterPath()
        australia.moveTo(0.8 * self.width(), 0.55 * self.height())
        australia.lineTo(0.9 * self.width(), 0.58 * self.height())
        australia.lineTo(0.85 * self.width(), 0.7 * self.height())
        australia.lineTo(0.75 * self.width(), 0.68 * self.height())
        australia.closeSubpath()
        painter.drawPath(australia)
    
    def draw_locations(self, painter):
        """绘制世界各地的节点"""
        for country, coords in WORLD_LOCATIONS.items():
            x = coords[0] * self.width()
            y = coords[1] * self.height()
            
            # 绘制节点
            node_size = 4
            
            # 如果该国家在攻击源统计中，增大节点大小
            if country in self.attack_stats["attacks_by_country"]:
                attack_count = self.attack_stats["attacks_by_country"][country]
                node_size = min(12, 4 + (attack_count / 10))
            
            # 绘制外圈
            painter.setPen(QPen(QColor(0, 200, 0, 150), 1))
            painter.setBrush(QBrush(QColor(0, 100, 0, 50)))
            painter.drawEllipse(QPointF(x, y), node_size, node_size)
            
            # 绘制内圈
            painter.setBrush(QBrush(QColor(0, 255, 0, 150)))
            painter.drawEllipse(QPointF(x, y), node_size/2, node_size/2)
            
            # 只为重要节点绘制国家名称
            if node_size > 5:
                # 设置文本样式
                painter.setPen(QPen(QColor(0, 255, 0, 200), 1))
                painter.setFont(QFont(DEFAULT_FONT, 8))
                # 绘制国家名称
                painter.drawText(QRectF(x - 40, y + node_size + 2, 80, 20), 
                                Qt.AlignHCenter | Qt.AlignTop, country)
    
    def draw_attacks(self, painter):
        """绘制攻击动画"""
        for attack in self.active_attacks:
            if not attack.active:
                continue
                
            current_pos = attack.get_current_position()
            
            # 设置攻击颜色
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(attack.color))
            
            # 绘制粒子
            painter.drawEllipse(QPointF(current_pos[0], current_pos[1]), 
                                attack.size, attack.size)
            
            # 绘制轨迹
            if attack.progress > 0.05:  # 当动画进行一段时间后才显示轨迹
                path = QPainterPath()
                path.moveTo(attack.source[0], attack.source[1])
                path.quadTo(attack.control_point[0], attack.control_point[1], 
                            current_pos[0], current_pos[1])
                
                # 设置轨迹渐变
                grad = QLinearGradient(attack.source[0], attack.source[1], 
                                       current_pos[0], current_pos[1])
                grad.setColorAt(0, QColor(attack.color.red(), attack.color.green(), 
                                          attack.color.blue(), 30))
                grad.setColorAt(1, QColor(attack.color.red(), attack.color.green(), 
                                          attack.color.blue(), 150))
                
                painter.setPen(QPen(grad, 2))
                painter.drawPath(path)
    
    def mousePressEvent(self, event):
        """鼠标按下事件，用于移动窗口和选择攻击"""
        if event.button() == Qt.LeftButton:
            # 检查是否点击了攻击粒子
            for attack in self.active_attacks:
                if attack.active:
                    pos = attack.get_current_position()
                    dist = math.sqrt((event.pos().x() - pos[0])**2 + (event.pos().y() - pos[1])**2)
                    if dist <= attack.size * 2:  # 增加点击区域以便更容易选中
                        self.selected_attack = attack
                        self.selected_attack_label.setText(f"攻击类型: {attack.attack_type}")
                        return
            
            # 如果没有点击攻击，则准备移动窗口
            # 注意：现在使用CustomTitleBar来处理窗口拖动
            pass
    
    def keyPressEvent(self, event):
        """键盘按键事件"""
        # Esc键关闭窗口或退出全屏
        if event.key() == Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                self.title_bar.maximize_button.setText("□")
            else:
                self.close()
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止线程
        if self.threat_thread.isRunning():
            self.threat_thread.stop()
            self.threat_thread.wait(1000)  # 等待最多1秒
            
        # 停止定时器
        self.animation_timer.stop()
        
        # 发送关闭信号
        self.closed.emit()
        
        super().closeEvent(event)


# 用于独立测试
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThreatMapWindow()
    window.show()
    sys.exit(app.exec_()) 