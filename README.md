# tuberscutter
Automatically seperate the silent parts from any video!

Do You make video content for internet but don't want to bore people with long silences in your clip and find using an editing software to do it manually too time consuming? Then you share the same problem with me, and this project aims to help you.

## What does it do to the video that I have gave it?
There is only one threshold value for detecting silent parts. This means, the program will interpret your video as a collection of *Silent* and *Loud* sub videos. In this interpretation a video might look like as such 

| Loud block 1 | Silent block 1 | Loud block 2 | Silent block 2 | Loud block 3 | ... | Loud block n | Silent block n |

of course, the video could end with a loud block:

| Loud block 1 | Silent block 1 | Loud block 2 | Silent block 2 | Loud block 3 | ... | Loud block n |

or, it could begin with a silent block

| Silent block 1 | Loud block 1 | Silent block 2 | Loud block 2 | Silent block 3 | ... | Silent block n | Loud block n |

and begin with a silent, end with a silent:

| Silent block 1 | Loud block 1 | Silent block 2 | Loud block 2 | Silent block 3 | ... | Silent block n |

This program detects Loud and Silent blocks and exports them as a bunch of short videos while preserving audio quality and image resolution.

Notice: Right now, it only exports Loud parts. I'll edit the code to achieve that, if you can do it, I would enjoy your contribution. 

## How to use it?
At the moment, your go-to file is **cutter.py**. It has a few command line arguments.

`python cutter.py --file test.mp4 -f .mov -d 1 -t -27`

`--file` is the input video; the video whose silent parts will be removed.

`-f` is the format of the output files: L0.mov, L1.mov, ... (.mp4 by default)

`-d` is the duration of the shortest detected silence. Unit in seconds. (0.3 sec by default.)

`-t` is the noise threshold. (-60 dB by default)

Currently the best arrangement of parameters for me is `-d 1 -t -27`. It could change depending on the video you have. So it is a little subjective at the moment. After implementing loudness normalization, it should be more or less usable by everyone.

There are 4 fields you can edit to your interest in **cutter.py** but since the program supports command line arguments, you won't need most of them.

`DEFAULT_DURATION = 0.3` units in seconds. Any silence shorter than 3/10 of a second will not be marked as silent block. (`-d`)

`DEFAULT_THRESHOLD = -60` units in dB. Anything louder than this will be marked as loud and vice versa. (`-t`)

`split_video("F:\\test.mov","L")`

*"L"* is the common label for naming Loud output files. The output would look like this "L0.mp4, L1.mp4, L2.mp4, L3.mp4, ...". If you edit it to *"Loud Block-"* then output will have the shape "Loud Block-0.mp4, Loud Block-1.mp4, Loud Block-2.mp4, Loud Block-3.mp4, ...". 
This program currently cannot output Silent parts so no customization for them.

### Running
You need three piece of software to use this program. 

*ffmpeg*: a general purpose video and audio manipulation software running from command line-> https://ffmpeg.org/

*python*: the interpreter for our "cutter.py" file -> https://www.python.org/

*ffmpeg-python*: ffmpeg itself is ugly, python itself is not designed specifically for editing. Python bindings for FFmpeg -> https://github.com/kkroening/ffmpeg-python

make sure the "ffmpeg" and "python" are added to PATH

https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10

https://geek-university.com/python/add-python-to-the-windows-path/

If everything is set, open the command prompt, [`cd`](https://www.wikiwand.com/en/Cd_(command)) to the directory which contains the *.py* file (and preferably your video file), type `python firstprototype.py`, hit return, YAY!

Program should start doing its job. It will produce files in the same folder where you run *.py* file.

## How did you do this? (i.e. Credits)

- Thank you carykh for inspiring me. I hope you like what I do. I love your videos! Check out his [YouTube channel](https://www.youtube.com/user/carykh) and [Github](https://github.com/carykh)
- Thank you FFmpeg developers for making this super flexible video editing monster.
- F\*ck you FFmpeg C libraries https://ffmpeg.org/doxygen/4.1/index.html (JK, I am just not a native speaker of C)
- Thank you [kkroening](https://github.com/kkroening) for saving me from programming in C and giving [this sweet piece of code](https://github.com/kkroening/ffmpeg-python/blob/master/examples/split_silence.py) that I've mutated to my purposes.

finally

- Thank *you* for your interest. Bye!
