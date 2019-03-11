#!/usr/bin/env python3

import os
import glob
import json

import gcp_ocr
import ms_azure_ocr
import abbyy_ocr


input_dir = './data'
output_dir = 'output'


def process(item):
    """Process image"""
    # Create folder
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_dir, os.path.basename(item).split('.')[0])
    os.makedirs(folder, exist_ok=True)
    # Save image
    os.popen('cp {} {}'.format(item, os.path.join(folder, os.path.basename(item))))

    for call_back in (gcp_ocr, ms_azure_ocr, abbyy_ocr):
        text, response = call_back.ocr(item)
        # Save text
        with open(os.path.join(folder, 'text_{}.txt'.format(call_back.__name__)), 'w') as f:
            f.write(text)
        # Save response
        with open(os.path.join(folder, 'response_{}.json'.format(call_back.__name__)), 'w') as f:
            json.dump(response, f)


def main():
    for item in glob.glob('{}{}*.*'.format(input_dir, os.path.sep)):
        process(item)


if __name__ == '__main__':
    main()

