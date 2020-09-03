import pyzed.sl as sl

def main():
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30

    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    img = sl.Mat()

    runtime_parameter = sl.RuntimeParameters()
    for i in range(50):
        if zed.grab(runtime_parameter) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(img, sl.VIEW.LEFT)
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)
            print("Image Resolution: {0} x {1} || Image timestamp {2}".format(img.get_width(), img.get_height(), timestamp.get_milliseconds()))

    zed.close()


if __name__ == "__main__":
    main()
