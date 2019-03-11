import requests


def ocr(image_path):
    """OCR from Microsoft azure.
    Tutorial available at https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/quickstarts/python-disk"""
    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = "d5c93f1c78794380ab7b9f65737aaa40"
    assert subscription_key

    # You must use the same region in your REST call as you used to get your
    # subscription keys. For example, if you got your subscription keys from
    # westus, replace "westcentralus" in the URI below with "westus".
    #
    # Free trial subscription keys are generated in the "westus" region.
    # If you use a free trial subscription key, you shouldn't need to change
    # this region.
    vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v2.0/"
    ocr_url = "{}ocr".format(vision_base_url)

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               "Content-Type": "application/octet-stream"}
    params = {'language': 'unk', 'detectOrientation ': 'true'}
    response = requests.post(ocr_url,
                             headers=headers,
                             params=params,
                             data=image_data)
    response.raise_for_status()

    analysis = response.json()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
    text = '\n'.join([x['text'] for x in word_infos])

    return text, analysis
