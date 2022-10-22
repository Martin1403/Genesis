FROM jozo/pyqt5

# App name
ARG APP="gui"

RUN apt-get update
RUN apt-get install -y alsa-base alsa-utils
RUN apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev
RUN apt-get install -y libpulse0 libasound2 libasound2-plugins libsndfile1-dev
RUN apt-get -y install ffmpeg
RUN apt-get install -y python3-pip

RUN mkdir $APP
COPY . $APP/
#COPY requirements.txt $APP/requirements.txt
#RUN pip install -U pip
RUN pip install -r $APP/requirements.txt

ENV DISPLAY=:0.0
ENV DOCKER=1

CMD python3 gui
