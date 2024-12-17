#!/bin/env python3

# PyQt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtPositioning import *

# Py
import os
import sys
import subprocess
import time
import random
import webbrowser
from datetime import date

# PyUSB
import usb.core
import usb.util

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("MOdin")
        pixcon = QPixmap('/home/navia/Documents/MOdin/variants/modin/ico.png')
        resized_pixcon = pixcon.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
        self.setWindowIcon(QIcon(resized_pixcon))
        self.about_window_instance = None


        # Main widget
        central_face_widget = QWidget(self)
        self.setCentralWidget(central_face_widget)

        # Layout - Main
        main_layout = QVBoxLayout(central_face_widget)
        v1 = QVBoxLayout()
        v2 = QVBoxLayout()
        v3 = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        tab = QTabWidget(self)

        # Menubar
        menbar = self.menuBar()
        mainbar = menbar.addMenu('&Options')
        help_bar = menbar.addMenu('&Help')
        about_menu = QAction('&About MOdin', self)
        help_bar.addAction(about_menu)
        about_menu.triggered.connect(self.about_window)
        about_menu.setShortcut('F1')


        # V1 Labels
        title = QLabel()
        title.setText("MOdin - Flashing tool on linux, for samsung devices (obviously powered by Odin4, but made it user friendly)\nFor now its in ALPHA TESTING")


        # Tab1
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        self.box = QTextEdit(self, placeholderText="Odin4's output")
        self.box.setReadOnly(True)
        self.statBTN = QPushButton()
        self.statBTN.setEnabled(False)
        self.statBTN.setText("Eepy (zzz) - Basically waiting for someone")
        self.statBTN.setStyleSheet("""
            QPushButton {
                color: black;
                font-style: bold;
            }
            QPushButton:disabled {
                color: black;
                font-style: bold;
            }
        """)
        BTNStat_Layout = QHBoxLayout()
        BTNStat_Layout.addWidget(self.statBTN)
        tab1_layout.addLayout(BTNStat_Layout)
        tab1_layout.addWidget(self.box)
        # BTN
        self.btn_diag = QTimer(self)
        self.btn_diag.timeout.connect(self.reset_BTNDIAG)
        self.btn_diag.start(8000)

        # Tab2
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout2 = QVBoxLayout()
        self.nandwipe = QCheckBox()
        self.nandwipe.setText("Nand Wipe (Also called, Clear userdata for some reason, which is reasonable)")
        where_odin = QLabel()
        self.where_odin_box = QLineEdit()
        self.where_odin_box.setText("/usr/bin/odin4")
        where_odin.setText("Odin4 Executable Binary Location")
        self.where_odin_box.setToolTip("This is where the Odin4 Binary executable is located. usually on /usr/bin/odin4. \nBut if its somewhere, you can input it here.")
        tab2_layout.addWidget(self.nandwipe)
        tab2_layout2.addWidget(where_odin)
        tab2_layout2.addWidget(self.where_odin_box)
        tab2_layout.addLayout(tab2_layout2)
        
        # Tab - tabs
        tab.addTab(tab1, "Odin's Output")
        tab.addTab(tab2, "Configure")

        # h1 - linebox and btns
        self.AP_file = QLineEdit()
        self.BL_file = QLineEdit()
        self.CSC_file = QLineEdit()
        self.CP_file = QLineEdit()
        self.UDATA_file = QLineEdit()
        AP_label = QLabel()
        AP_label.setText("AP: ")
        BL_label = QLabel()
        BL_label.setText("BL: ")
        CSC_label = QLabel()
        CSC_label.setText("CSC: ")
        CP_label = QLabel()
        CP_label.setText("CP: ")
        UDATA_label = QLabel()
        UDATA_label.setText("Userdata: ")
        self.AP_btn = QPushButton()
        self.AP_btn.setText("Select AP")
        self.AP_btn.clicked.connect(lambda: self.select_file(self.AP_file))
        self.BL_btn = QPushButton()
        self.BL_btn.setText("Select BL")
        self.BL_btn.clicked.connect(lambda: self.select_file(self.BL_file))
        self.CSC_btn = QPushButton()
        self.CSC_btn.setText("Select CSC")
        self.CSC_btn.clicked.connect(lambda: self.select_file(self.CSC_file))
        self.CP_btn = QPushButton()
        self.CP_btn.setText("Select CP")
        self.CP_btn.clicked.connect(lambda: self.select_file(self.CP_file))
        self.UDATA_btn = QPushButton()
        self.UDATA_btn.setText("Select UD")
        self.UDATA_btn.clicked.connect(lambda: self.select_file(self.UDATA_file))
        self.flashbtn = QPushButton()
        self.flashbtn.setText("Flash")
        self.flashbtn.clicked.connect(self.flash_device)

        # h1 - responding layouts
        APLayout = QHBoxLayout()
        APLayout.addWidget(AP_label)
        APLayout.addWidget(self.AP_file)
        APLayout.addWidget(self.AP_btn)
        BLLayout = QHBoxLayout()
        BLLayout.addWidget(BL_label)
        BLLayout.addWidget(self.BL_file)
        BLLayout.addWidget(self.BL_btn)
        CSCLayout = QHBoxLayout()
        CSCLayout.addWidget(CSC_label)
        CSCLayout.addWidget(self.CSC_file)
        CSCLayout.addWidget(self.CSC_btn)
        CPLayout = QHBoxLayout()
        CPLayout.addWidget(CP_label)
        CPLayout.addWidget(self.CP_file)
        CPLayout.addWidget(self.CP_btn)
        UDATALayout = QHBoxLayout()
        UDATALayout.addWidget(UDATA_label)
        UDATALayout.addWidget(self.UDATA_file)
        UDATALayout.addWidget(self.UDATA_btn)

        # Layout placing
        main_layout.addLayout(v1)
        v1.addWidget(title)
        v1.addLayout(h1)
        h1.addWidget(tab)
        h1.addLayout(v2)
        v2.addLayout(APLayout)
        v2.addLayout(BLLayout)
        v2.addLayout(CSCLayout)
        v2.addLayout(CPLayout)
        v2.addLayout(UDATALayout)
        v2.addWidget(self.flashbtn)



        self.show()

    def about_window(self):
        if self.about_window_instance is None or not self.about_window_instance.isVisible():
            self.about_window_instance = AboutWindow()
        self.about_window_instance.show()
        self.about_window_instance.raise_()
        self.about_window_instance.activateWindow()



        # Start checking for USB devices periodically
        self.usb_timer = QTimer(self)
        self.usb_timer.timeout.connect(self.check_usb_devices)
        self.usb_timer.start(5000)  # Check every 5 seconds

    def reset_BTNDIAG(self):
        pick = random.choice(['1', '2', '3', '4'])
        if pick == '1':
            self.statBTN.setText("Eepy(zzz) - Waiting for a samsung device on Download mode")
            self.statBTN.setStyleSheet("""
                QPushButton {
                    color: black;
                    font-style: bold;
                }
                QPushButton:disabled {
                    color: black;
                    font-style: bold;
                    background-color: white;
                }
            """)
        elif pick == '2':
            self.statBTN.setText("Eepy(zzz) - Are you sure that your samsung phone is in download mode?")
            self.statBTN.setStyleSheet("""
                QPushButton {
                    color: black;
                    font-style: bold;
                }
                QPushButton:disabled {
                    color: black;
                    font-style: bold;
                    background-color: white;
                }
            """)
        elif pick == '3':
            self.statBTN.setText("Eepy(zzz) - SCAMSUNG")
            self.statBTN.setStyleSheet("""
                QPushButton {
                    color: black;
                    font-style: bold;
                }
                QPushButton:disabled {
                    color: black;
                    font-style: bold;
                    background-color: white;
                }
            """)
        elif pick == '4':
            self.statBTN.setText("Eepy(zzz) - Did you know that this tool's predecessor was a super image downloader?")
            self.statBTN.setStyleSheet("""
                QPushButton {
                    color: black;
                    font-style: bold;
                }
                QPushButton:disabled {
                    color: black;
                    font-style: bold;
                    background-color: white;
                }
            """)

    def select_file(self, line_edit):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Firmware Files (*.tar *.lz4 *.img *.tar.md5)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            line_edit.setText(selected_file)

    def flash_device(self):
        self.usb_timer.stop()  # Stop USB detection
        self.btn_diag.stop()
        self.statBTN.setText("Flashing...")
        self.statBTN.setStyleSheet("""
            QPushButton {
                color: black;
                font-style: bold;
            }
            QPushButton:disabled {
                color: black;
                font-style: bold;
                background-color: blue;
            }
        """)
        command = ["odin4"]
        if self.AP_file.text():
            command.extend(["-a", self.AP_file.text()])
        if self.BL_file.text():
            command.extend(["-b", self.BL_file.text()])
        if self.CSC_file.text():
            command.extend(["-s", self.CSC_file.text()])
        if self.CP_file.text():
            command.extend(["-c", self.CP_file.text()])
        if self.UDATA_file.text():
            command.extend(["-u", self.UDATA_file.text()])
        if self.nandwipe.isChecked():
            command.append("-e")

        if len(command) > 1:  # If at least one file is provided
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    self.box.append(output.strip())
            error = process.stderr.read()
            if error:
                self.box.append("Error:\n" + error.strip())
                self.statBTN.setText("FAIL")
                self.statBTN.setStyleSheet("""
                    QPushButton {
                        color: black;
                        font-style: bold;
                    }
                    QPushButton:disabled {
                        color: black;
                        font-style: bold;
                        background-color: red;
                    }
                """)
        else:
            self.box.append("No files selected for flashing.")
            self.statBTN.setText("FAIL")
            self.statBTN.setStyleSheet("""
                QPushButton {
                    color: black;
                    font-style: bold;
                }
                QPushButton:disabled {
                    color: black;
                    font-style: bold;
                    background-color: red;
                }
            """)
            
        self.btn_diag.start(8000)
        self.usb_timer.start(5000)  # Resume USB detection

    def check_usb_devices(self):
        device = usb.core.find(idVendor=0x04e8)  # Samsung Vendor ID
        if device:
            if "Download Mode" in usb.util.get_string(device, device.iSerialNumber):
                # The box and BTN are just for eyecandy
                self.box.append("Samsung device in Download Mode detected!")
                self.statBTN.setText("DEVICE IN DOWNLOAD MODE")
                self.statBTN.setStyleSheet("""
                    QPushButton {
                        color: black;
                        font-style: bold;
                    }
                    QPushButton:disabled {
                        color: white;
                        font-style: bold;
                        background-color: purple;
                    }
                """)
            else:
                self.box.append("Samsung device detected, but not in Download Mode.")

class AboutWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('About MOdin')

        # Main Widget
        central_face_ui = QWidget(self)
        self.setCentralWidget(central_face_ui)

        self.image_label = None

        # Contents
        self.image = QPixmap('/home/navia/Documents/MOdin/variants/modin/ico.png')
        if not self.image.isNull():
            processed_image = self.image.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label = QLabel()
            self.image_label.setPixmap(processed_image)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            print('Logo not found')
        title = QLabel()
        title.setText("MOdin")
        title.setStyleSheet("""
        QLabel {
            font-family: bold;
        }                    
        """)
        version_id = QLabel()
        version_id.setText("v0.1 - @Mizumo-prjkt/MizProject\n\nPyQt6")
        version_id.setStyleSheet("""
        QLabel {
            font-family: monospace;
        }                         
        """)
        description = QLabel()
        description.setText("A simple tool for flashing Samsung devices.")
        btn_license = QPushButton()
        btn_license.setText("License")
        btn_license.clicked.connect(self.open_license)
        btn_source = QPushButton()
        btn_source.setText("Source Code")
        btn_source.clicked.connect(self.open_source)


        # Layout - About window
        self.alayout = QVBoxLayout()
        v1 = QVBoxLayout()
        h1 = QHBoxLayout()
        v2 = QVBoxLayout()
        v3 = QVBoxLayout()
        central_face_ui.setLayout(self.alayout)
        self.alayout.addLayout(v1)
        v1.addLayout(h1)
        h1.addWidget(self.image_label)
        h1.addLayout(v2)
        v2.addWidget(title)
        v2.addWidget(version_id)
        v2.addWidget(description)
        v2.addWidget(btn_license)
        v2.addWidget(btn_source)


        self.show()
        
    def open_license(self):
        license_widget = QDialog(self)
        license_widget.setWindowTitle("License")
        layout = QVBoxLayout()
        license = QLabel()
        cyear = date.today().year
        license.setText(f"""
{cyear} - MizProject
This Software License is in MIT, guaranteed that there is no warranty on the software, obtaining code is free without any reprocussion as TLDR.

This software is not affiliated with Samsung Electronics.

Other Open Source Projects used
Note: Mentions of '(built-in)' means that the licenses is integrated via the software that Mizumo-prjkt or MizProject
has no control of (odin4)

- PyQt6
  (c) Riverbank Computing, Ltd.
  Licensed: GNU GPL3

- LZ4
  (c) LZ4 Group, 2011-2016 Yann Collet
  Odin4 (built-in)
  Licensed: MIT

- Crypto++ Library from Boost Software
  (c) Boost Software
  Odin4 (built-in)
  Licensed: Boost Software License

  
For more info about the licenses, check the license file attached to the project
""")
        layout.addWidget(license)
        license_widget.setLayout(layout)
        license_widget.exec()


    def open_source(self):
        webbrowser.open("https://github.com/MizProject")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
