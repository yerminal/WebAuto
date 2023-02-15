# WebAuto
## INSTALLATION 
### WINDOWS
1. [Download](https://chromedriver.chromium.org/downloads) the windows version of the chromedriver supporting your current chrome version. Extract the chromedriver.exe.

2. [Download](https://drive.google.com/drive/folders/1_qwjkghJwksdBrpm7oBnVJ1GarhZBuqx?usp=share_link) all ```ffmpeg.exe``` ```ffplay.exe``` ```ffprobe.exe```.

3. Extract the repo zip.

4. Copy and paste ```ffmpeg.exe``` ```ffplay.exe``` ```ffprobe.exe``` into the repo folder.

5. Paste ```chromedriver.exe``` to the folder named ```webdriver``` in the repo folder.

6. Install the required python packages using pip.
```bash
pip install -r requirements.txt
```
### LINUX
1. If you don't have the ffmpeg package (you can check by typing ```ffmpeg -version```), follow the installation directions (Ubuntu) on [this website](https://phoenixnap.com/kb/install-ffmpeg-ubuntu).

2. [Download](https://chromedriver.chromium.org/downloads) the linux64 version of the chromedriver supporting your current chrome version. Extract the chromedriver.

3. Extract the repo zip and paste ```chromedriver``` to the folder named ```webdriver``` in the repo folder.

4. Install the required python packages using pip.
```bash
pip install -r requirements.txt
```
## TEST
1. Run main_test.py.
```bash
python main_test.py
```
2. You can run multiples of main.py. Just open up another terminal and type the same command.
```bash
python main_test.py
```
## RUN
### ADDING COURSE
1. Enter your lesson list and credentials into the data.py
2. Run main.py.
```bash
python main.py
```
3. You can run multiples of main.py. Just open up another terminal and type:
```bash
python main.py
```
### CHANGE SECTION
1. Enter your lesson list into the change_section.py.
2. Run change_section.py.
```bash
python change_section.py
```
