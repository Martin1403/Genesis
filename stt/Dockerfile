FROM python:3.9-slim

# App name
ARG APP="stt"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

# If you want to have scorer (990Mb):
RUN apt-get update
RUN apt-get -y install p7zip-full
RUN 7za x stt/model/archive/output_graph.scorer.7z.001 -ostt/model/


# Settings:
ENV QUART_APP=$APP.app:app
ENV QUART_ENV=development
EXPOSE 5001

CMD quart run -h "0.0.0.0" -p 5001