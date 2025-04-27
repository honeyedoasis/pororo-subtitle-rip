import json
import os
import warnings

import cv2
import pytesseract

import re

from pororo import Pororo
from pororo.pororo import SUPPORTED_TASKS
from utils.image_util import plt_imshow, put_text

warnings.filterwarnings('ignore')

SUBFILENAME_ID = 'Filename'
SUBSTART_ID = 'Start'
SUBEND_ID = 'End'
SUBHANGUL_ID = 'Hangul'
SUBENGLISH_ID = 'English'


class PororoOcr:
    def __init__(self, model: str = "brainocr", lang: str = "ko", **kwargs):
        self.model = model
        self.lang = lang
        self._ocr = Pororo(task="ocr", lang=lang, model=model, **kwargs)
        self.img_path = None
        self.ocr_result = {}

    def run_ocr(self, img_path: str, debug: bool = False):
        self.img_path = img_path
        self.ocr_result = self._ocr(img_path, detail=True)

        if self.ocr_result['description']:
            ocr_text = self.ocr_result["description"]
        else:
            ocr_text = "No text detected."

        if debug:
            self.show_img_with_ocr()

        return ocr_text

    @staticmethod
    def get_available_langs():
        return SUPPORTED_TASKS["ocr"].get_available_langs()

    @staticmethod
    def get_available_models():
        return SUPPORTED_TASKS["ocr"].get_available_models()

    def get_ocr_result(self):
        return self.ocr_result

    def get_img_path(self):
        return self.img_path

    def show_img(self):
        plt_imshow(img=self.img_path)

    def show_img_with_ocr(self):
        img = cv2.imread(self.img_path)
        roi_img = img.copy()

        for text_result in self.ocr_result['bounding_poly']:
            text = text_result['description']
            tlX = text_result['vertices'][0]['x']
            tlY = text_result['vertices'][0]['y']
            trX = text_result['vertices'][1]['x']
            trY = text_result['vertices'][1]['y']
            brX = text_result['vertices'][2]['x']
            brY = text_result['vertices'][2]['y']
            blX = text_result['vertices'][3]['x']
            blY = text_result['vertices'][3]['y']

            pts = ((tlX, tlY), (trX, trY), (brX, brY), (blX, blY))

            topLeft = pts[0]
            topRight = pts[1]
            bottomRight = pts[2]
            bottomLeft = pts[3]

            cv2.line(roi_img, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(roi_img, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(roi_img, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(roi_img, bottomLeft, topLeft, (0, 255, 0), 2)
            roi_img = put_text(roi_img, text, topLeft[0], topLeft[1] - 20, font_size=15)

            # print(text)

        plt_imshow(["Original", "ROI"], [img, roi_img], figsize=(16, 10))


def get_settings():
    with open('settings.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def make_timings(filename, decimal_char):
    start_end = filename.split('__')
    start_arr = start_end[0].split('_')
    start = '0' + start_arr[0] + ':' + start_arr[1] + ':' + start_arr[2] + decimal_char + start_arr[3]
    end_arr = start_end[1].split('_')
    end_arr.pop()
    end = '0' + end_arr[0] + ':' + end_arr[1] + ':' + end_arr[2] + decimal_char + end_arr[3]
    return [start, end]


def make_rows_korean(image_directory, debug=False):
    ocr = PororoOcr()

    full_output = []

    srt_index = 0
    total_files = len(os.listdir(image_directory))
    print('OCR for Hangul with Pororo')
    for filename in os.listdir(image_directory):
        f = os.path.join(image_directory, filename)
        if os.path.isfile(f):
            sub_timings = make_timings(filename, ',')  # for srt
            sub_content_arr = ocr.run_ocr(f, debug=False)
            if len(sub_content_arr) >= 1:
                sub_content = "\n".join(sub_content_arr)
            else:
                sub_content = 'NO TEXT FOUND'

            output = {
                SUBFILENAME_ID: filename,
                SUBSTART_ID: sub_timings[0],
                SUBEND_ID: sub_timings[1],
                SUBHANGUL_ID: sub_content
            }

            full_output.append(output)

            srt_index += 1
            print('LINE', srt_index, '/', total_files)
            print(sub_content + '\n')

            if debug and srt_index >= 5:
                break

    return full_output

def remove_hangul(text):
    return re.sub(r'[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7A3]', '', text)

def make_rows_english(image_directory, debug=False):
    print('OCR for Tesseract for English')

    pytesseract.pytesseract.tesseract_cmd = get_settings()['tesseract_exe']

    full_output = []

    srt_index = 0
    total_files = len(os.listdir(image_directory))
    for filename in os.listdir(image_directory):
        f = os.path.join(image_directory, filename)
        if os.path.isfile(f):
            sub_index = str(srt_index)
            sub_timings = make_timings(filename, ',')  # for srt
            lang = 'kor+eng'
            sub_content = str(pytesseract.image_to_string(f, lang=lang)).strip()

            new_content = []
            for line in sub_content.split('\n'):
                # line = remove_hangul(line)
                # if len(line.strip()) == 0:
                #     continue

                new_content.append(line)

            if len(new_content) == 0:
                sub_content = 'NO TEXT FOUND'
            else:
                sub_content = '\n'.join(new_content)

            if len(sub_content) == 0:
                sub_content = ''

            output = {
                SUBFILENAME_ID: filename,
                SUBSTART_ID: sub_timings[0],
                SUBEND_ID: sub_timings[1],
                SUBHANGUL_ID: sub_content
            }

            full_output.append(output)

            srt_index += 1
            print(f'LINE {srt_index} / {total_files}')
            print(sub_content + '\n')

            if debug and srt_index >= 5:
                break

    return full_output


def make_srt_from_rows(rows, project_id):
    os.makedirs('output', exist_ok=True)
    with open(f'output/{project_id}.srt', 'w', newline='', encoding='utf-8') as srtfile:
        index = 0
        for row in rows:
            srtfile.write(str(index) + '\n')

            timing = row[SUBSTART_ID] + ' --> ' + row[SUBEND_ID]
            srtfile.write(timing + '\n')

            srtfile.write(row[SUBHANGUL_ID] + '\n' + '\n')
            index += 1


def fix_rows(rows):
    out_rows = []

    num_rows = len(rows)
    i = 0
    while i < num_rows:
        print(i)
        curr = rows[i]
        next_different = i + 1
        while next_different < num_rows:
            next_row = rows[next_different]
            if next_row[SUBHANGUL_ID] == curr[SUBHANGUL_ID]:
                # print('Merging ', curr, next_row)
                next_different += 1
            else:
                break

        if next_different - 1 != i:
            last_merge = rows[next_different - 1]
            curr[SUBEND_ID] = last_merge[SUBEND_ID]

        # print('Adding', i, curr)
        out_rows.append(curr)
        i = next_different

    return out_rows


def main():
    settings = get_settings()
    my_project_id = settings['project_name']
    my_image_directory = settings['vsf_img_dir']

    if settings['use_english']:
        rows = make_rows_english(my_image_directory)
    else:
        rows = make_rows_korean(my_image_directory)

    rows = fix_rows(rows)

    make_srt_from_rows(rows, my_project_id)


if __name__ == "__main__":
    main()
