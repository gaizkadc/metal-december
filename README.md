# metal-december
Metal December posts an album from a JSON file to Instagram and Twitter every day during December.

## Environment variables
Some env vars can be provided in an `.env` file:
```
APP_NAME=metal-december

IMG_WIDTH=1080
IMG_HEIGHT=1350
COVER_WIDTH=700
BORDER_WIDTH=50

ALL_IMGS=0

LOGS_FOLDER_PATH=logs
JSON_FOLDER=json
IMGS_FOLDER=img
FONTS_PATH=fonts
COVERS_PATH=covers

TWITTER_POST=1
INSTAGRAM_POST=1

OUTPUT_FORMAT=jpg // intabot fails to upload png imgs

TWITTER_CONSUMER_KEY=<consumer key>
TWITTER_CONSUMER_SECRET=<consumer secret>
TWITTER_ACCESS_TOKEN=<access token>
TWITTER_ACCESS_TOKEN_SECRET=<access token secret>

IG_USERNAME=<username>
IG_PASSWORD=<password>
```