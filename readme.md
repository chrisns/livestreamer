# Camera streamer
The intention of this is to add a live stream on youtube and then stream a given url to it.
I use it on my Synology disk station to broadcast my security cameras to a private stream so that I can see them anywhere and take advantage of youtube's offsite recording of my surveillance footage.

## pre-reqs
You'll need a `client_secrets.json` file that looks like:
```json
{
  "installed": {
    "client_id": "xxxx.apps.googleusercontent.com",
    "client_secret": "xxx",
    "redirect_uris": [
      "http://localhost",
      "urn:ietf:wg:oauth:2.0:oob"
    ],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```
populate the client_id and client_secret accordingly see https://developers.google.com/api-client-library/python/guide/aaa_client_secrets and https://cloud.google.com/console for getting those

First run will log in, you'll need to interactively login with that, it'll give you a link which will present a code to input into the python lib.

You'll need to make sure there is a volume mount for `/conf` after the first run you can probably make it readonly


# Run
Something along the lines of this should help:

```bash
docker run \
  --rm \
  -ti \
  -v $(pwd)/config:/conf \
  -e BROADCAST_TITLE=external-driveway \
  -e BROADCAST_URL=rtsp://syno:111@192.168.0.1:554/Sms=1.unicast\
  chrisns/livestreamer
```