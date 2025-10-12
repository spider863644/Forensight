# Forensight

Forensight is an advanced image OSINT toolkit for investigative and analytical workflows. It allows you to extract metadata, perform reverse searches, detect objects and faces, run OCR, and handle a variety of image formats, all from the command line.

## Features

**Forensight** is a comprehensive image OSINT toolkit designed for investigators, analysts, and researchers. Its features include:

### Core Image Handling
- Read, write, and manipulate images in multiple formats, including advanced formats like AVIF.
- Resize, crop, rotate, and convert images.
- Compute image hashes for duplicate detection or similarity analysis.

### Metadata & Reverse Search
- Extract and analyze EXIF/XMP metadata from images.
- Restore missing or corrupted metadata.
- Perform automated reverse image searches.
- Retrieve geolocation, timestamps, and other embedded information.

### AI-Powered Analysis (Optional)
- Detect objects and people in images.
- Recognize scenes and generate descriptive captions.
- Classify images and extract visual features.
- Supports GPU acceleration for faster processing (optional).

### Face Recognition
- Detect and identify faces in images.
- Count faces and highlight them with bounding boxes.
- Compare faces against reference datasets for identification.

### OCR (Optical Character Recognition)
- Extract printed and handwritten text from images.
- Recognize multi-language text depending on configuration.

### Data Handling & Visualization
- Analyze numeric and tabular data associated with images.
- Map geolocated images and generate interactive visualizations.
- Create detailed investigation reports.

### Security, Signing & Encryption
- Sign images or investigation data for integrity verification.
- Encrypt sensitive files to protect investigation materials.
- Validate signatures to ensure authenticity.

### CLI Utilities
- User-friendly command-line interface for workflow automation.
- Display progress, logs, and status updates in the terminal.
- Combine multiple operations (e.g., metadata extraction + OCR + face detection) in a single run.
- Flexible argument parsing for customized workflows.

## Screenshots & Workflow

### Screenshot
![Forensight Screenshot](Forensight.png)  
*Example of Forensight running a metadata extraction and OCR workflow.*

### Workflow GIF
![Forensight Workflow](assets/workflow.gif)  
*Demonstrates a full workflow: metadata extraction → OCR → face detection → mapping.*


## Installation for windows
### Step 1: Open PowerShell as Administrator

Press Win + X → Windows Terminal (Admin) or search for PowerShell, right-click → Run as administrator.

### Step 2: Install Git via winget
```
winget install --id Git.Git -e --source winget
```
--id Git.Git → Specifies the official Git package
-e → Exact match

--source winget → Ensures it uses the official repository

### Step 3: Verify Installation

```
git --version
```

You should see something like:

> git version 2.41.0.windows.1

## Download Python (3.11 is recommended) 

### Step 1: Go to the official Python website: 
https://www.python.org/downloads/windows/

 Click Download Python 3.11

 ### Step 2: Run the Installer

1. Open the downloaded .exe file.


2. Important: Check “Add Python 3.11 to PATH” at the bottom.


3. Click Install Now.


4. Wait for the installation to complete and click Close.

## Cloning repository

### Step 1: Open Git Bash and clone the repository

Press Win, type Git Bash, and open it.

```
git clone https://github.com/spider863644/Forensight.git
cd Forensight
```

### Step 2: Set up a Python environment
```
python -m venv venv
venv\Scripts\activate          
```
### Step 3: Install dependencies

```
pip install -r requirements.txt
```

> Important for Windows users: Installing face_recognition on Windows can be tricky because it depends on dlib. Follow these steps carefully:

> 1. Install Visual Studio Build Tools 2019 or 2022 (ensure "Desktop development with C++" workload is selected).


> 2. Download the precompiled wheel for dlib that matches your Python version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#dlib.


> 3. Install the wheel manually, e.g.:


>
```
pip install path\to\dlib-19.24.0-cp311-cp311-win_amd64.whl
```

> 4. Finally, install face_recognition:

>
```
pip install face_recognition
```


## Installation for Linux 

### Step 1: Install Git and Python3
```
sudo apt update && sudo apt upgrade
```
```
sudo apt install git
```
```
sudo apt install python3
```

### Step 2: Clone the repository
```
git clone https://github.com/spider863644/Forensight.git
cd Forensight
```
### Step 3: Set up a Python environment
```
python -m venv venv
source venv/bin/activate 
```

### Step 4: Install dependencies
```
sudo apt update
```
```
sudo apt install tesseract-ocr -y
```
```
pip install -r requirements.txt
```

### Step 5: Install Face_recognition
```
sudo apt install -y cmake g++ make python3-dev
sudo apt install -y libboost-all-dev
```
Now simply run 

```
pip install face_recognition
```
## Usage:
```
python3 main.py --help       #Linux

python main.py --help    #Winndows

```

## Contributing

Forensight is for personal and educational purposes.
Please do not redistribute, modify, or use it commercially without permission.
Credit must always be given to the original author.

## Author & Credits

Forensight was conceptualized, developed, and maintained by Spider Anongreyhat.

All core code, workflows, and OSINT techniques implemented in this project are the work of the author.

Special thanks to the developers of the libraries used: Pillow, OpenCV, face_recognition, YOLOv8, BLIP, pytesseract, and others that made this toolkit possible.

> “Built for investigative and educational OSINT. Always give credit where it’s due.” 
