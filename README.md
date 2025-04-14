<h2 align="center">
Pororo subtitle rip
</h2>

# Installation

1. Download this repository (click the green code button > download zip)
1. Install VideoSubFinder: https://sourceforge.net/projects/videosubfinder/
1. Install python 3.8: https://www.python.org/downloads/release/python-3810/
1. Install pycharm (optional if you know how to install python): https://www.jetbrains.com/pycharm/
1. (Optional) Install tesseract for english subtitle detection: https://github.com/UB-Mannheim/tesseract/wiki

# Usage

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

VideoSubFinder exports 3 types of images:
* RGB
* ILA
* ISA

I dunno what the difference between ILA and ISA is but basically you want to look at each of them and see which one has the best results.

Now open the images in some image viewer and delete all the badly recognized ones.

## 2. Running the script to generate the srt file

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

### 2.2. Running in pycharm

1. Download pycharm: https://www.jetbrains.com/pycharm/ 
2. In pycharm, choose this folder to open as a new project
3. There should be a popup asking you to install requirements, click accept
4. Run the file by clicking on this bug looking icon to the right of the arrow in the top bar
5. After running, it will export the .srt to `output/project_name`

![run.jpeg](assets%2Fimages%2Frun.jpeg)