FROM python:3.7-slim

# App name
ARG APP="ai"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

# Settings:
ENV QUART_APP=$APP.app:app
ENV QUART_ENV=development
EXPOSE 5002

CMD quart run -h "0.0.0.0" -p 5002