#!/usr/bin/python
import httplib2
import os
import sys
import datetime
import pprint

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "/conf/client_secrets.json"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("/conf/%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# Create a liveBroadcast resource and set its title, scheduled start time,
# scheduled end time, and privacy status.
def insert_broadcast(youtube, options):
  insert_broadcast_response = youtube.liveBroadcasts().insert(
    part="snippet,status,contentDetails",
    body=dict(
      snippet=dict(
        title=options.broadcast_title,
        scheduledStartTime=options.start_time,
        scheduledEndTime=options.end_time
      ),
      contentDetails=dict(
        enableEmbed=True,
        enableDvr=True,
        enableAutoStart=True
      ),
      status=dict(
        privacyStatus=options.privacy_status
      )
    )
  ).execute()

  snippet = insert_broadcast_response["snippet"]

  print "Broadcast '%s' with title '%s' was published at '%s'." % (
    insert_broadcast_response["id"], snippet["title"], snippet["publishedAt"])
  return insert_broadcast_response["id"]

# Create a liveStream resource and set its title, format, and ingestion type.
# This resource describes the content that you are transmitting to YouTube.
def insert_stream(youtube, options):
  insert_stream_response = youtube.liveStreams().insert(
    part="snippet,cdn",
    body=dict(
      snippet=dict(
        title=options.stream_title
      ),
      cdn=dict(
        format="1080p",
        ingestionType="rtmp"
      )
    )
  ).execute()

  snippet = insert_stream_response["snippet"]

  print "Stream '%s' with title '%s' was inserted." % (
    insert_stream_response["id"], snippet["title"])
  return insert_stream_response

# Bind the broadcast to the video stream. By doing so, you link the video that
# you will transmit to YouTube to the broadcast that the video is for.
def bind_broadcast(youtube, broadcast_id, stream_id):
  bind_broadcast_response = youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=broadcast_id,
    streamId=stream_id
  ).execute()

  print "Broadcast '%s' was bound to stream '%s'." % (
    bind_broadcast_response["id"],
    bind_broadcast_response["contentDetails"]["boundStreamId"])

if __name__ == "__main__":
  argparser.add_argument("--broadcast-title", help="Broadcast title",
    default="New Broadcast")
  argparser.add_argument("--privacy-status", help="Broadcast privacy status",
    default="private")
  argparser.add_argument("--start-time", help="Scheduled start time",
    default=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
  argparser.add_argument("--end-time", help="Scheduled end time",
    default=(datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S.000Z"))
  argparser.add_argument("--stream-title", help="Stream title",
    default="New Stream")
  args = argparser.parse_args()

  youtube = get_authenticated_service(args)
  
  broadcast_id = insert_broadcast(youtube, args)
  stream = insert_stream(youtube, args)
  bind_broadcast(youtube, broadcast_id, stream["id"])
  f= open("/tmp/streamname.txt","w+")
  f.write(stream["cdn"]["ingestionInfo"]["streamName"])
  f.close() 
