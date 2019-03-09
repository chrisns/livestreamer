FROM python:2-alpine
RUN apk add --no-cache ffmpeg
RUN pip install --upgrade \
  google-api-python-client \
  google-auth \
  google-auth-oauthlib \
  google-auth-httplib2 \
  oauth2client
WORKDIR /app
COPY run.py run.sh /app/ 
ENV BROADCAST_TITLE ""
ENV BROADCAST_URL ""
VOLUME /conf
CMD ./run.sh