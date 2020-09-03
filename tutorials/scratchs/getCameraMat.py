import pyzed.sl as sl
import cv2
import numpy as np

def main():
    zed = sl.Camera()

    initParams = sl.InitParameters()
    initParams.camera_resolution = sl.RESOLUTION.HD720
    initParams.camera_fps = 30

    err = zed.open(initParams)
    if err != sl.ERROR_CODE.SUCCESS: exit(1)

    mat = sl.Mat()
    runtimeParameters = sl.RuntimeParameters()
    key = " "

    while key != 113:
        if zed.grab(runtimeParameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(mat, sl.VIEW.SIDE_BY_SIDE)
            imgData = mat.get_data()

            cv2.imshow("test", imgData)

        key = cv2.waitKey(5)


    zed.close()


if __name__ == "__main__":
    main()
