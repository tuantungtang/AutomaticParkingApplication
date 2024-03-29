
from predict import *
from findcam import *


def imageProcess():
    # type_read = predict_model()
    # license_read = license()
    type_read='ab'
    license_read="99 H77060"
    if type_read == findCamera()[2] and license_read == findCamera()[1]:
        return "true"
    return "false"


if __name__ == '__main__':
    print(imageProcess())
