GUI PyQT5
=========

### Venv:
###### python3.9
```bash
python -m venv gui/.venv && \
source gui/.venv/bin/activate && \
pip install -U pip && \
pip install -r gui/requirements.txt
```
### Run:
```bash
source gui/.venv/bin/activate && \
pyuic5 gui/lib/untitled.ui -o gui/lib/untitled.py && \
python gui
```
### Dev:
```bash
pyuic5 gui/lib/untitled.ui -o gui/lib/untitled.py
pyrcc5 data/icons/images.qrc -o images_rc.py 
```
**Note:**
Convert UI and QRC file.
### Display:
```bash
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
xhost +
```
### Docker:
```bash
docker build -t gui .
docker run --rm -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    -u qtuser \
    gui python3 /gui/app.py
``` 

### Development:
```bash
# Run container:
docker container run --rm -it --name gui --device /dev/snd:/dev/snd ubuntu:22.04 bash

# Install dependencies: (inside container)
apt-get update && \
apt-get install -y alsa-base alsa-utils && \
# apt-get install -y pulseaudio && \
apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y && \
apt-get install -y libpulse0 libasound2 libasound2-plugins libsndfile1-dev && \
apt-get -y install ffmpeg && \
apt-get install -y python3-pip build-essential python3 python3-dev

# Copy files: (outside container)
docker cp requirements.txt $(docker ps -aqf "name=gui"):tmp/ && \
docker cp lib/vad_test.py $(docker ps -aqf "name=gui"):tmp/ && \
docker cp lib/daemon.conf $(docker ps -aqf "name=gui"):etc/pulse/

# Install requirements: (inside container)
pip install -r tmp/requirements.txt && \
pulseaudio -D && \
python3 tmp/vad_test.py

# Delete:
docker rm $(docker ps -aq) -f  # All containers
docker network prune 
docker volume prune
```
**Note:**
Trying to use audio in docker container.
  

**### Tests:**
```bash
python -m doctest --option ELLIPSIS --verbose notes/code.rst
```

###### [Links:]()
- [Link](https://github.com/jozo/docker-pyqt5) PyQt5 inside Docker
- [Link](https://pypi.org/project/halo/) Halo spinner
- [Link](https://stackoverflow.com/questions/45700653/can-my-docker-container-app-access-the-hosts-microphone-and-speaker-mac-wind) Microphone in docker container
- [Link](https://askubuntu.com/questions/138611/how-to-change-audio-bit-depth-and-sampling-rate) Pulseaudio settings (sample rate, channels)
- [Link](https://stackoverflow.com/questions/34496882/get-docker-container-id-from-container-name) Docker container id from name 
- 