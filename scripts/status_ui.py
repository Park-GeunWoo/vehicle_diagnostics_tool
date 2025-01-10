#!/usr/bin/python3
# -*- coding: utf-8 -*-
import rospy
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from std_msgs.msg import Float32, Int8MultiArray
from message_filters import ApproximateTimeSynchronizer, Subscriber


class SystemMonitorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_components()
        self.init_layout()
        self.init_style()
        self.init_msgs_sync()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)
        
    def init_components(self):
        self.cpu_usage_sub = Subscriber('/sys_status/cpu_usage', Float32)
        self.cpu_freq_sub = Subscriber('/sys_status/cpu_freq', Float32)
        self.gpu_usage_sub = Subscriber('/sys_status/gpu_usage', Float32)
        self.memory_sub = Subscriber('/sys_status/memory', Float32)

        self.cpu_usage_val = 'N/A'
        self.cpu_freq_val = 'N/A'
        self.gpu_usage_val = 'N/A'
        self.memory_percent_val = 'N/A'

        self.cpu_usage_label = QLabel(self.cpu_usage_val)
        self.cpu_freq_label = QLabel(self.cpu_freq_val)
        self.gpu_usage_label = QLabel(self.gpu_usage_val)
        self.memory_percent_label = QLabel(self.memory_percent_val)

        self.status_list_sub = Subscriber('/sensor_status/sensor_status_bool', Int8MultiArray)
        self.lidar_status = QFrame()
        self.gps_status = QFrame()
        self.camera_status = QFrame()
        self.lidar_label = QLabel("Lidar")
        self.gps_label = QLabel("GPS")
        self.camera_label = QLabel("Camera")

        self.button_1 = QPushButton("Start")
        self.button_2 = QPushButton("Stop")
        self.button_3 = QPushButton("Reset")
        self.button_1.clicked.connect(self.start_clicked)
        self.button_2.clicked.connect(self.stop_clicked)
        self.button_3.clicked.connect(self.reset_clicked)

    def init_layout(self):
        """set layout, container"""
        main_layout = QVBoxLayout(self)

        '''button layout'''
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_1)
        button_layout.addWidget(self.button_2)
        button_layout.addWidget(self.button_3)
        button_layout.setSpacing(10)
        
        button_container = QFrame()
        button_container.setFixedHeight(50)
        button_layout.setAlignment(Qt.AlignLeft)
        button_container.setLayout(button_layout)

        '''sys grid'''
        sys_layout = QGridLayout()
        sys_layout.addWidget(self.cpu_usage_label, 0, 1)
        sys_layout.addWidget(self.cpu_freq_label, 1, 1)
        sys_layout.addWidget(self.gpu_usage_label, 2, 1)
        sys_layout.addWidget(self.memory_percent_label, 3, 1)

        sys_container = QFrame()
        sys_container.setLayout(sys_layout)
        sys_container.setFrameShape(QFrame.Box)
        sys_container.setLineWidth(2)
        
        '''def grid'''
        def_layout = QGridLayout()
        def_layout.addWidget(QLabel('Nothing'), 0, 0)
        
        def_container = QFrame()
        def_container.setLayout(def_layout)
        def_container.setFrameShape(QFrame.Box)
        def_container.setLineWidth(2)
        
        '''sensor grid'''
        sensor_layout = QGridLayout()
        sensor_layout.addWidget(self.lidar_status, 0, 0)
        sensor_layout.addWidget(self.gps_status, 1, 0)
        sensor_layout.addWidget(self.camera_status, 2, 0)
        
        sensor_layout.addWidget(self.lidar_label, 0, 1)
        sensor_layout.addWidget(self.gps_label, 1, 1)
        sensor_layout.addWidget(self.camera_label, 2, 1)

        sensor_container = QFrame()
        sensor_container.setLayout(sensor_layout)
        sensor_container.setFrameShape(QFrame.Box)
        sensor_container.setLineWidth(2)
        
        main_grid_layout = QGridLayout()
        main_grid_layout.addWidget(sys_container, 0, 0, 1, 1)
        main_grid_layout.addWidget(def_container, 0, 2, 4, 1)
        main_grid_layout.addWidget(sensor_container, 0, 3, 2, 1)
        
        grid_container = QFrame()
        grid_container.setLayout(main_grid_layout)
        
        main_layout.addWidget(button_container)
        main_layout.addWidget(grid_container)

    def init_style(self):
        '''setting label, box style'''
        labels = [self.cpu_usage_label, self.cpu_freq_label, self.gpu_usage_label, self.memory_percent_label]
        
        for label in labels:
            font =label.font()
            font.setPointSize(15)
            font.setBold(True)
            label.setFont(font)
        
        labels = [self.lidar_label, self.gps_label, self.camera_label]
        
        for label in labels:
            font =label.font()
            font.setPointSize(15)
            font.setBold(True)
            label.setFont(font)
            
        sensor_box = [self.lidar_status, self.gps_status, self.camera_status]
        
        for box in sensor_box:
            box.setFrameShape(QFrame.Box)
            box.setFixedSize(50, 50)
            box.setLineWidth(2)
        
        self.button_1.setFixedSize(100,40)
        self.button_2.setFixedSize(100,40)
        self.button_3.setFixedSize(100,40)
        
    def sys_status_callback(self, cpu_usage, cpu_freq, gpu_usage, memory, status_list):
        #update status values
        self.cpu_usage_val = f"{cpu_usage.data:.2f}%"
        self.cpu_freq_val = f"{cpu_freq.data:.2f} GHz"
        self.gpu_usage_val = f"{gpu_usage.data:.2f}%"
        self.memory_percent_val = f"{memory.data:.2f}%"

        if bool(status_list.data[0]):
            lider_c = 'background-color: green;'
        else:
            lider_c = 'background-color: red;'
        
        if bool(status_list.data[1]):
            gps_c = 'background-color: green;'
        else:
            gps_c = 'background-color: red;'
            
        if bool(status_list.data[2]):
            camera_c = 'background-color: green;'
        else:
            camera_c = 'background-color: red;'
            
        self.lidar_status.setStyleSheet(lider_c)
        self.gps_status.setStyleSheet(gps_c)
        self.camera_status.setStyleSheet(camera_c)
        
    def update_ui(self):
        """UI 업데이트 로직"""
        self.cpu_usage_label.setText(f"CPU: {self.cpu_usage_val}")
        self.cpu_freq_label.setText(f"CPU Frequency: {self.cpu_freq_val}")
        self.gpu_usage_label.setText(f"GPU: {self.gpu_usage_val}")
        self.memory_percent_label.setText(f"Memory: {self.memory_percent_val}")

    def start_clicked(self):
        print("Start clicked")

    def stop_clicked(self):
        print("Stop clicked")

    def reset_clicked(self):
        print("Reset clicked")

    def init_msgs_sync(self):
        ats = ApproximateTimeSynchronizer(
            [self.cpu_usage_sub, self.cpu_freq_sub, self.gpu_usage_sub, self.memory_sub, self.status_list_sub],
            queue_size=20,
            slop=1,
            allow_headerless=True
        )
        ats.registerCallback(self.sys_status_callback)
        
if __name__ == '__main__':
    SystemMonitorGUI()