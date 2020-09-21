from importlib import import_module
import os
from flask import Flask, render_template, Response, send_file
import time
import picamera
from camera import Camera

app = Flask(__name__)
def cameraRaw():
    with picamera.PiCamera(sensor_mode=2) as camera:

        stream = BytesIO()

        camera.resolution = (2592,1944)
        camera.iso = 800
        time.sleep(2)

        camera.framerate = 5
        #camera.rotation = 90
        camera.start_preview()
        #camera.shutter_speed = camera.exposure_speed
        camera.shutter_speed =0
        camera.exposure_mode = 'auto'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g

        time.sleep(5)
        camera.capture(stream, 'jpeg', bayer=True)
        start_time = time.time()
        d = RPICAM2DNG()
        output = d.convert(stream)
        print("--- %s seconds ---" % (time.time() - start_time))
        with open('image.dng', 'wb') as f:
                f.write(output)
        time.sleep(5)
        camera.stop_preview()

def cameraJpeg():
    with picamera.PiCamera(sensor_mode=2) as camera:
        camera.resolution = (2592,1944)
        #camera.rotation = 90
        #camera2.start_preview()
        # Camera warm-up time
        time.sleep(1)
        camera.capture('foo2.jpg')
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/picture', methods=['POST','GET'])
def basic():
    with picamera.PiCamera(sensor_mode=2) as camera:
        camera.resolution = (2592,1944)
        camera.rotation = 90
        #camera2.start_preview()
        # Camera warm-up time
        time.sleep(1)
        camera.capture('foo3.jpg')
    return send_file('./foo3.jpg', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', threaded=True)
