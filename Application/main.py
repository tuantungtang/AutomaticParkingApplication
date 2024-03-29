import os

import cv2
from PyQt5.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QVBoxLayout
from interface1 import Ui_MainWindow

import mysql.connector


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.pixmapItem = None
        self.setupUi(self)
        self.connect_to_database()
        self.predict_and_display_result()
        self.setFixedSize(900, 600)

    def connect_to_database(self):
        config = {
            'user': 'root',
            'password': '123456',
            'database': 'gx',
            'host': 'localhost',
            'raise_on_warnings': True,
        }

        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM thongtinxe LIMIT 1")
            rows = cursor.fetchall()  # Lấy tất cả các hàng từ kết quả truy vấn
            for row in rows:
                # Thêm các giá trị vào từng QListWidget tương ứng
                self.ID.addItem(str(row[0]))
                self.ownerName.addItem(row[1])
                self.Barcode.addItem(row[2])

        except mysql.connector.Error as err:
            print(err.msg)

    def predict_and_display_result(self):

        self.capture = cv2.VideoCapture(0)
        self.dimensions = self.capture.read()[1].shape[1::-1]
        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)
        view = QGraphicsView(self)
        view.setScene(scene)
        layout = QVBoxLayout(self)
        layout.addWidget(view)

        # Lấy kích thước của QGraphicsView2
        view_rect = self.graphicsView_2.viewport().rect()
        self.graphicsView_2.setScene(scene)

        # Hiển thị ảnh T3 trên QGraphicsView

        pixmap = QPixmap(*self.dimensions)
        scene = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)
        # Lấy kích thước của QGraphicsView
        view_rect = self.graphicsView.viewport().rect()
        pixmap_rect = pixmap_item.boundingRect()
        self.graphicsView.setScene(scene)

    def get_frame(self):
        _, frame = self.capture.read()
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    # os.remove("LPTemp.jpg")
    # os.remove("TM.jpg")
    sys.exit(app.exec())
