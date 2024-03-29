import cv2
from connectToMysql import *
from pyzbar import pyzbar
# from tensorflow.keras.preprocessing.image import image

def findCamera():
    # Khởi tạo capture từ camera
    cap = cv2.VideoCapture(0)

    # Loop để liên tục chụp hình
    while True:
        # Đọc frame hiện tại
        ret, frame = cap.read()

        # Decode mã vạch trong frame
        decoded_objects = pyzbar.decode(frame)
        print(decoded_objects)
        # Hiển thị frame
        cv2.imshow("Barcode Scanner", frame)

        # Loop qua các đối tượng đã decode và in ra dữ liệu
        for obj in decoded_objects:
            # Gọi hàm connect với dữ liệu từ mã vạch
            return connect(obj.data.decode('utf-8'))

        # Chờ phím nhấn để thoát
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # Giải phóng camera và đóng tất cả các cửa sổ
    cap.release()


if __name__ == '__main__':
    print(findCamera())
