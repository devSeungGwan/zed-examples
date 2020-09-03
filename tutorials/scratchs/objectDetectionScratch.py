import pyzed.sl as sl
import cv2
import numpy as np

def main():
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_units = sl.UNIT.METER
    init_params.sdk_verbose = True


    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS: exit(1)


    obj_param = sl.ObjectDetectionParameters()
    obj_param.enable_tracking = True
    obj_param.image_sync = True
    obj_param.enable_mask_output = True


    camera_infos = zed.get_camera_information()
    if obj_param.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        positional_tracking_param.set_floor_as_origin = True
        zed.enable_positional_tracking(positional_tracking_param)


    print("Object Detection: Loading Module...")


    err = zed.enable_object_detection(obj_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        zed.close()
        exit(1)

    objects = sl.Objects()
    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 40

    while zed.grab() == sl.ERROR_CODE.SUCCESS:
        err = zed.retrieve_objects(objects, obj_runtime_param)

        if objects.is_new:
            obj_array = objects.object_list

            print("{0} Object(s) Detected".format(str(len(obj_array))))

            if len(obj_array) > 0:
                first_object = obj_array[0]

                print("First object attributes:")
                print("Label {0} (Conf. {1}/100)".format(
                    repr(first_object.label),
                    repr(first_object.confidence))
                )

            if obj_param.enable_tracking:
                print("Tracking ID: {0}, Tracking state: {1}/{2}".format(
                    str(int(first_object.id))
                    , repr(first_object.tracking_state)
                    , repr(first_object.action_state)
                ))


            position = first_object.position
            velocity = first_object.velocity
            dimension = first_object.dimensions

            print("3D Position: [{0},{1},{2}]\nVelocity: [{3},{4},{5}]\n3D Dimension: [{6},{7},{8}]".format(
                position[0]
                , position[1]
                , position[2]
                , velocity[0]
                , velocity[1]
                , velocity[2]
                , dimension[0]
                , dimension[1]
                , dimension[2]
            ))

            if first_object.mask.is_init():
                    print("2D Mask Available")

            print("Bounding Box 2D")
            bounding_box = first_object.bounding_box

            for it in bounding_box:
                    print("     {}".format(str(it), end=''))


            input('\nPress enter to continue: ')

    zed.close()

if __name__ == "__main__": main()
