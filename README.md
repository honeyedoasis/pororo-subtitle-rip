<h2 align="center">
Pororo subtitle rip
</h2>

# Installation

1. Download this repository (click the green code button > download zip)
1. Install VideoSubFinder: https://sourceforge.net/projects/videosubfinder/
1. Install python 3.8: https://www.python.org/downloads/release/python-3810/
1. Install pycharm (cos I dunno how to properly setup `requirements.txt`..): https://www.jetbrains.com/pycharm/
1. Sign up for google vision and 

# Usage

## 0. Google Vision

**NOTE: In order to use google vision you need to provide your credit or debit card details to google**

This project relies on google vision.

You can sign up for a free trial and after the trial ends you get 1000 free tokens per month. This is equivalent to 1000 lines translated each month.

To sign up and setup google vision follow the instructions here:

1. https://cloud.google.com/vision/docs/ocr follow the `Start Free` instructions
2. https://cloud.google.com/vision/docs/setup

## 1. Video Sub Finder

### 1.1 Adjust the settings

* Open the settings tab
* Adjust the setting, set the bounds of where the subtitles are expected to be.
* If your subtitles are always the same colour, you can filter by color. See the color of the pixel by hovering your cursor over the video, and it will display in the bottom right. To check the filtered image, hold down `T`.
  * You may need to play around with the gamma to get it to detect better or expand the default dL/ dA / dB

![vsf1.jpg](assets%2Fimages%2Fvsf1.jpg)

### 1.2 Run the search

* Now in the Search tab click Run Search
  * If you have run it earlier, you will want to clear folders first

![vsf-2.jpg](assets%2Fimages%2Fvsf-2.jpg)

### 1.3 Choose and delete the bad images

* Open VideoSubFinder/RGBImages. Open the images in some image viewer and delete all the incorrect ones. 
* You can delete duplicates if you want to save on google cloud tokens (but you will need to manually fix the timing later).

## 2 Install Requirements

### 2.1 Settings.json

In the folder there is a `settings.json` file that looks like this

```json
{
    "project_name": "my_project_name",
    "vsf_img_dir": "C:/Programs/Tools/VideoSubFinder_6.10_x64/ILAImages",
    "tesseract_exe": "C:/Programs/Tesseract-OCR/tesseract.exe",
    "use_english": false
}
```
* project_name: this is what your srt file will be named as
* vsf_img_dir: the video sub finder image directory, which should match the one you chose earlier in [Step 1.3](#13-choose-and-delete-the-bad-images)
* tesseract_exe: (OPTIONAL) the path to your tesseract installation (for english)
* use_english: toggle if you want to detect english subtitles

### 2.2 Installing pycharm

1. Download pycharm: https://www.jetbrains.com/pycharm/ 
2. In pycharm, choose this folder to open as a new project
3. There should be a popup asking you to install requirements, click accept

## 3. Running the script to generate the srt file

### 3.1 Generating raw subtitles

1. Open main.py
1. Run the file by clicking on this bug looking icon to the right of the arrow in the top bar
3. After running, it will export the .srt to `output/{project_name}.srt`

![run.jpeg](assets%2Fimages%2Frun.jpeg)

## 4 Translating the subtitles

### 4.1 Cleaning and exporting the subtitles

1. Open your subtitle file `output/{project_name}.srt` in some editor and remove any incorrectly detected text 
3. Once you are done open in Subtitle Edit and go to `File > Export > Plain Text`
4. Match the settings to the image below and save this file (to be used in the next step)

![export-txt-settings.png](assets/images/export-txt-settings.png)

### 4.2 Translating using Gemini

1. Go to https://aistudio.google.com/prompts/new_chat
2. Copy the content of `prompt.txt` into here
   * Describe the video in the prompt (where it says `- Context: {desciption}`
   * Remove the speaker part of the prompt if the subtitles don't have them
5. Paste the contents file you exported in the previous step below the prompt. The format of the prompt should look like this:

```
Translate these Korean subtitles to english.

- Context: Behind the scenes of the recent fromis_9 album "Like You Better". fromis_9 is made of 5 members, Lee Chaeyoung, Park Jiwon, Song Hayoung, Baek Jiheon and Lee Nagyung. Non of the ex-members (Jisun, Saerom, Gyuri, Seoyeon) will be mentioned in this video!

- Keep each line brief and easy to read, like how real subtitles appear

- Make sure to use the same format as provided:

\```
LINE NUM
TRANSLATION

LINE NUM
TRANSLATION

cont.
\```

- When translating 1. Do not put ending full stops 2. Strip out korean characters used for emotions such as ㅋㅋㅋㅋ or ㅠㅠ from the translation

- Do not delete merge or skip lines

---

1
NG: Hello, everyone. This is Nagyung

2
Thank you all for coming
to the dinner I prepared
```

6. Save the output from gemini inside `pororo-subtitle-rip/gemini/{project_id}.gemini`


### 4.3 Generating the translated subtitles

In order to generate the translated subtitle we need 2 files to be located inside the gemini folder
1. `gemini/{project_id}.gemini` (copied from step 4.2)
2. `gemini/{project_id}.srt` (copied from step 3)

After you have these 2 files open `conv-translation.py` and run

The translated subtitle file will be generated at `gemini/{project_id}.en.srt` 