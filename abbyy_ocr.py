import time
from abbyy_utils import *


def ocr(image_path):
    """OCR from ABBY
    Tutorial available at https://www.ocrsdk.com/documentation/quick-start-guide/python-ocr-sdk/"""
    processor = AbbyyOnlineSdk()

    print("Uploading..")
    settings = ProcessingSettings()
    task = processor.process_image(image_path, settings)
    if task is None:
        print("Error")
        return
    if task.Status == "NotEnoughCredits":
        print("Not enough credits to process the document. Please add more pages to your application's account.")
        return

    print("Id = {}".format(task.Id))
    print("Status = {}".format(task.Status))

    # Wait for the task to be completed
    print("Waiting..")
    # Note: it's recommended that your application waits at least 2 seconds
    # before making the first getTaskStatus request and also between such requests
    # for the same task. Making requests more often will not improve your
    # application performance.
    # Note: if your application queues several files and waits for them
    # it's recommended that you use listFinishedTasks instead (which is described
    # at http://ocrsdk.com/documentation/apireference/listFinishedTasks/).

    while task.is_active():
        time.sleep(5)
        print(".")
        task = processor.get_task_status(task)

    print("Status = {}".format(task.Status))

    if task.Status != "Completed":
        return '', ''

    if not task.DownloadUrl:
        return '', ''

    get_result_url = task.DownloadUrl

    if not get_result_url:
        return '', ''

    file_response = requests.get(get_result_url, stream=True)
    text = '\n'.join([i.strip() for i in file_response.content.decode().split('\r\n') if i.strip()])
    return text, text
