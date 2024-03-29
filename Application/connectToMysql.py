
import mysql.connector
from mysql.connector import Error

config = {
    'user': 'root',
    'password': 'djinndien123',
    'database': 'test_python_connect',
    'host': 'localhost',
    'raise_on_warnings': True,
    'auth_plugin': 'mysql_native_password'
}

def connect(mssv):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(prepared=True)
        query = "SELECT * FROM sv WHERE idsv  = %s"
        cursor.execute(query, (mssv,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            print("Không tìm thấy dữ liệu cho mssv", mssv)
        # cursor.close()
        # cnx.close()
    except Error as e:
        print("Error:", e)

if __name__ == '__main__':
    print(connect('27211223958'))
