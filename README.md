# substoforced
Extracting forced subtitles from a full subtitle with a set of timecodes

# Installation
```sh
git clone https://github.com/pcroland/substoforced
cd substoforced
pip install -r requirements.txt
```

# Usage
```
❯ ./stf.py -h
substoforced 1.0.0

USAGE: stf.py [-h] [-v] [-s SUB] [-f FOLDER]

FLAGS:
  -h, --help                  show this help message.
  -v, --version               show version.
  -s, --sub SUB               specifies srt input
  -f, --folder FOLDER         specifies a folder where SubsMask2Img generated timecodes (optional)
                              you should remove the junk from there manually
```

# Generating hardsub timecodes with AviSynth
Example:
```c++
FFMS2("X:\path\to\video.mkv")
InpaintDelogo(Loc="300,830,-300,-80", Show=4, DynMask=4, DynTune=210, DynMask4H=120)
SubsMask2Img(ImgInflate=1, ImgDir="X:\path\to\folder")
```
- `Loc` defines where hardsubs should be, you can set it up with `Crop()`
- `ImgDir` is where hardsub timecodes will be saved
- InpaintDelogo picks up signs with text from the video and credits text so remove those manually
- run `.avs` script with [`AVSMeter`](https://forum.doom9.org/showthread.php?t=174797)
