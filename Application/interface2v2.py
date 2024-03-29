import os
import cv2
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene

from TensorFlow.TVT.DVNT import license_read_from


class CameraThread(QtCore.QThread):
    change_pixmap_signal_cam1 = QtCore.pyqtSignal(QtGui.QImage)
    change_pixmap_signal_cam2 = QtCore.pyqtSignal(QtGui.QImage)
    result_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.save_image = False

    def run(self):
        maSV = "27211200906"
        loaiXe = "ab"
        bienSoXe = "81S120224"
        cap_cam1 = cv2.VideoCapture(0)  # Camera trên máy tính

        # Camera từ URL
        cap_cam2 = cv2.VideoCapture('http://172.25.102.156:8080/video')

        finalResult = ""
        while True:
            ret1, frame1 = cap_cam1.read()
            ret2, frame2 = cap_cam2.read()

            if ret1:
                qt_img1 = self.convert_cv_qt(frame1)
                if self.save_image:
                    cv2.imwrite("test/license_temp.jpg", frame1)
                    ketqua = license_read_from()
                    print(ketqua)
                    os.remove("test/license_temp.jpg")
                    finalResult=finalResult+maSV+","+loaiXe+","+ ketqua + ","
                    if bienSoXe == ketqua:
                        finalResult = finalResult + "true"
                    else:
                        finalResult = finalResult + "false"
                    print(finalResult)
                    self.result_signal.emit(finalResult)
                    self.save_image = False
                    finalResult=""
                self.change_pixmap_signal_cam1.emit(qt_img1)

            if ret2:
                qt_img2 = self.convert_cv_qt(frame2)
                # if self.save_image == True:
                #     cv2.imwrite("test/type_temp.jpg", frame2)
                self.change_pixmap_signal_cam2.emit(qt_img2)

            # Đợi một khoảng thời gian ngắn trước khi cập nhật hình ảnh tiếp theo
            self.msleep(50)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        return qt_img


class CameraView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setFixedSize(550, 400)  # Đặt kích thước cố định cho camera

    def update_image(self, qt_img):
        pixmap = QPixmap.fromImage(qt_img)

        # Lấy kích thước của khung camera_view_1
        frame_width = self.width()
        frame_height = self.height()

        # Căn chỉnh kích thước hình ảnh để phù hợp với khung
        pixmap_resized = pixmap.scaled(frame_width, frame_height, Qt.AspectRatioMode.KeepAspectRatio)

        self.scene().clear()
        self.scene().addPixmap(pixmap_resized)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_P:
            # Gửi tín hiệu để lưu ảnh từ cả hai camera
            camera_thread.save_image = True


class Ui_MainWindow(object):
    def update_result_label(self, result_text):
        try:
            # nhận kết quả trả về, chuyển sang mảng
            resultArray = result_text.split(",")
            # set lại ô ID theo kết quả trả về
            self.ID.clear()
            self.ID.addItem(resultArray[0])
            # set lại ô loại xe theo kết quả trả về
            self.typeV.clear()
            self.typeV.addItem(resultArray[1])
            # set lại ô biển số xe theo kết quả trả về
            self.Barcode.clear()
            self.Barcode.addItem(resultArray[2])
            # hiển thị thông báo đúng sai
            strR = resultArray[3]
            if (strR == "true"):
                # self.result.setText(_translate("MainWindow", "true", "khong tim thay"))
                self.result.setStyleSheet("background-color: ##33FF99")
                self.result.setText("true")
            else:
                self.result.setStyleSheet("background-color: #FF0033")
                self.result.setText("false")

        except Exception as e:
            print("Error in update_result_label:", str(e))
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        MainWindow.setStyleSheet("\n"
                                 "background-color: #fff;\n"
                                 "\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setStyleSheet("\n"
                                         "#headerL,#headerR {\n"
                                         "background-color: #00a08b;\n"
                                         "color:#fff;\n"
                                         "height:70px;\n"
                                         "font-weight:900;\n"
                                         "font-size:14px;\n"
                                         "border-radius:5px;\n"
                                         "}\n"
                                         "QLabel{\n"
                                         "margin-top:10px;\n"
                                         "font-size:15px;\n"
                                         "background-color: #fff;\n"
                                         "color:#00a08b;\n "
                                         "font-weight:700;\n"
                                         "}\n"
                                         "QListWidget{\n"
                                         "border-radius:3px;\n"
                                         "border:1px solid  rgb(94, 94, 94);\n"
                                         "background-color: #fff ;\n"
                                         "font-size:20px;\n"
                                         "}\n"
                                         "QListWidget:hover{\n"
                                         "border-color:#00a08b;\n"
                                         "}\n"
                                         "QGraphicsView{\n"
                                         "border-radius:3px;\n"
                                         "border: 1px solid #808080;\n "
                                         "}\n"
                                         "QPushButton{\n"
                                         "border-radius:3px;\n"

                                         "}\n"
                                         "#result{\n"
                                         "color:#fff;\n"
                                         "font-weight:700;\n"
                                         "height:50px;\n "
                                         "font-size:25px;\n "
                                         "background-color: #03a84e ;\n"
                                         "}"
                                         )
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_4 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_4.setStyleSheet("")
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lb_nameApp = QtWidgets.QLabel(parent=self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_nameApp.sizePolicy().hasHeightForWidth())
        self.lb_nameApp.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(99)
        self.lb_nameApp.setFont(font)
        self.frame_4.setStyleSheet("max-height:50px;\n")
        self.lb_nameApp.setStyleSheet("font-size:45px;\n"
                                      "color:#00a08b;\n"
                                      "font-weight:1200;\n"
                                      "")
        self.lb_nameApp.setObjectName("lb_nameApp")
        self.horizontalLayout.addWidget(self.lb_nameApp)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame_4)
        self.pushButton_3.setStyleSheet("")
        self.pushButton_3.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/car4.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout_4.addWidget(self.frame_4, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_4.addSpacing(50)
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 9, 0, 90)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headerR = QtWidgets.QLabel(parent=self.frame_2)
        self.headerR.setMinimumSize(QtCore.QSize(200, 70))
        self.headerR.setMaximumSize(QtCore.QSize(16777215, 70))
        self.headerR.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.headerR.setAutoFillBackground(False)
        self.headerR.setStyleSheet("")
        self.headerR.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.headerR.setScaledContents(False)
        self.headerR.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headerR.setWordWrap(False)
        self.headerR.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.headerR.setObjectName("headerR")
        self.verticalLayout_2.addWidget(self.headerR)
        self.lb_ID = QtWidgets.QLabel(parent=self.frame_2)
        self.lb_ID.setObjectName("lb_ID")

        self.verticalLayout_2.addWidget(self.lb_ID, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.ID = QtWidgets.QListWidget(parent=self.frame_2)
        self.ID.setMinimumSize(QtCore.QSize(100, 35))
        self.ID.setMaximumSize(QtCore.QSize(16777215, 35))
        self.ID.setObjectName("ID")
        self.verticalLayout_2.addWidget(self.ID)
        self.lb_typeV = QtWidgets.QLabel(parent=self.frame_2)
        self.lb_typeV.setObjectName("lb_typeV")
        self.verticalLayout_2.addWidget(self.lb_typeV, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.typeV = QtWidgets.QListWidget(parent=self.frame_2)
        self.typeV.setMaximumSize(QtCore.QSize(16777215, 30))
        self.typeV.setObjectName("typeV")
        self.verticalLayout_2.addWidget(self.typeV)
        self.lb_licensePlate = QtWidgets.QLabel(parent=self.frame_2)
        self.lb_licensePlate.setObjectName("lb_licensePlate")
        self.verticalLayout_2.addWidget(self.lb_licensePlate, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.Barcode = QtWidgets.QListWidget(parent=self.frame_2)
        self.Barcode.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Barcode.setObjectName("Barcode")
        self.verticalLayout_2.addWidget(self.Barcode)
        self.widget = QtWidgets.QWidget(parent=self.frame_2)
        self.widget.setMinimumSize(QtCore.QSize(0, 100))
        self.widget.setObjectName("widget")
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.line = QtWidgets.QFrame(parent=self.frame_3)
        self.line.setMinimumSize(QtCore.QSize(2, 0))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.frame = QtWidgets.QFrame(parent=self.frame_3)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.headerL = QtWidgets.QLabel(parent=self.frame)
        self.headerL.setMinimumSize(QtCore.QSize(200, 70))
        self.headerL.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(62)
        self.headerL.setFont(font)
        self.headerL.setStyleSheet("")
        self.headerL.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.headerL.setScaledContents(False)
        self.headerL.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.headerL.setObjectName("headerL")
        self.verticalLayout_3.addWidget(self.headerL)
        self.lb_graphicsView = QtWidgets.QLabel(parent=self.frame)
        self.lb_graphicsView.setStyleSheet("margin-top:10px;")
        self.lb_graphicsView.setObjectName("lb_graphicsView")
        # Thêm lb_graphicsView vào verticalLayout_3
        self.verticalLayout_3.addWidget(self.lb_graphicsView)

        # Create Camera Views
        self.camera_view_1 = CameraView()
        self.camera_view_2 = CameraView()

        # Tạo một QHBoxLayout mới để chứa hai CameraView
        self.horizontalLayout_camera = QtWidgets.QHBoxLayout()

        # Thêm camera_view_1 và camera_view_2 vào horizontalLayout_camera
        self.horizontalLayout_camera.addWidget(self.camera_view_1)
        self.horizontalLayout_camera.addWidget(self.camera_view_2)

        # Thêm horizontalLayout_camera vào verticalLayout_3
        self.verticalLayout_3.addLayout(self.horizontalLayout_camera)

        self.lb_result = QtWidgets.QLabel(parent=self.frame)
        self.lb_result.setObjectName("lb_result")
        self.verticalLayout_3.addWidget(self.lb_result)
        self.result = QtWidgets.QPushButton(parent=self.frame)

        self.result.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(62)
        self.result.setFont(font)

        self.result.setObjectName("result")
        self.verticalLayout_3.addWidget(self.result)
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout_4.insertWidget(1, self.frame_3)  # Di chuyển frame_3 lên trên
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lb_nameApp.setText(_translate("MainWindow", "Automatic Parking Application"))
        self.headerR.setText(_translate("MainWindow", " THÔNG TIN ĐĂNG KÝ XE "))
        self.lb_ID.setText(_translate("MainWindow", "ID"))
        self.lb_typeV.setText(_translate("MainWindow", "Loại xe"))
        self.lb_licensePlate.setText(_translate("MainWindow", "Biển số xe"))
        self.headerL.setText(_translate("MainWindow", "THÔNG TIN  KIỂM TRA"))
        self.lb_graphicsView.setText(_translate("MainWindow", "Hình ảnh"))
        self.lb_result.setText(_translate("MainWindow", "KẾT QUẢ"))
        self.result.setText(_translate("MainWindow", "True"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    camera_thread = CameraThread()
    camera_view_1 = ui.camera_view_1
    camera_view_2 = ui.camera_view_2
    # Connect the result signal to the update_result_label method
    camera_thread.result_signal.connect(ui.update_result_label)

    camera_thread.change_pixmap_signal_cam1.connect(camera_view_1.update_image)
    camera_thread.change_pixmap_signal_cam2.connect(camera_view_2.update_image)

    camera_thread.start()
    MainWindow.resize(1500, 800)
    MainWindow.show()
    sys.exit(app.exec())
