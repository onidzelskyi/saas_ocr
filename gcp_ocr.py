"""
 Example of using OCR from google 
 https://cloud.google.com/vision/docs/request
 
0. Set up your credentials
  export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
  echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  sudo apt-get update && sudo apt-get install google-cloud-sdk
  gcloud init
  export GOOGLE_APPLICATION_CREDENTIALS="/home/ubuntu/hera/EAST/hera-ocr-891d901f2af1.json"

1. Create POST body  
{
  'requests': [
    {
      'image': {
        'source': {
          'imageUri': 'http://fvi.flyaps.com:8888/data/image1.jpeg'
        }
      },
      'features': [
        {
          'type': 'TEXT_DETECTION'
        }
      ]
    }
  ]
}

 curl -X POST      \
 -H "Authorization: Bearer "$(gcloud auth application-default print-access-token)      \
 -H "Content-Type: application/json; charset=utf-8"      \
 --data @/tmp/del.json \
 "https://vision.googleapis.com/v1/images:annotate"
"""

import io
import json

from google.cloud import vision
from google.protobuf.json_format import MessageToJson


def ocr(image_path):
    """OCR from GCP.
    Tutorial available at https://cloud.google.com/vision/"""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    data = json.loads(MessageToJson(response))
    return data['textAnnotations'][0]['description'], data
