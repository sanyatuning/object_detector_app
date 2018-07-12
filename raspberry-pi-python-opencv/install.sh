#!/bin/sh

apt-get update
apt-get install -y \
        curl \
        libjpeg62 libtiff5 libpng12-0 libjasper1 \
        libgtk2.0-0 \
        libavcodec56 libavformat56 libswscale3 libv4l-0 \
        libatlas-base-dev gfortran

pip install --no-cache-dir numpy

curl -L "https://github.com/jabelone/OpenCV-for-Pi/raw/master/latest-OpenCV.deb" -o latest-OpenCV.deb
dpkg -i latest-OpenCV.deb

cp /usr/local/lib/python3.4/dist-packages/cv2.cpython-34m.so \
   /usr/lib/python3/dist-packages/cv2.cpython-34m.so
