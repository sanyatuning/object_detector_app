FROM resin/qemux86-64-python:3.5

RUN apt-get update -q
RUN apt-get install -q build-essential git cmake pkg-config \
    libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev \
    libgtk2.0-dev \
    unzip

RUN pip install -q tensorflow==1.5 Image opencv-python matplotlib numpy

#ADD https://github.com/Itseez/opencv/archive/3.1.0.zip /opencv.zip
ADD opencv.zip /opencv.zip

#ADD https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip /opencv_contrib.zip
ADD opencv_contrib.zip /opencv_contrib.zip

RUN unzip -q opencv.zip
RUN unzip -q opencv_contrib.zip

RUN mkdir /opencv-3.1.0/build
WORKDIR /opencv-3.1.0/build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib-3.1.0/modules \
	-D PYTHON_DEFAULT_EXECUTABLE=/usr/local/bin/python3 \
	-D BUILD_EXAMPLES=ON ..

RUN pip install -q redis

ADD object_detection /app/object_detection
ADD utils /app/utils
ADD *.py /app/

WORKDIR /app


CMD python3 -u object_detection_app.py -num-w 1