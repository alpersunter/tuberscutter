# GET CHUNK TIMES OF AN AUDIO CLIP
import ffmpeg
import re
import subprocess
import sys

silence_start_re = re.compile(' silence_start: (?P<start>[0-9]+(\.?[0-9]*))$')
silence_end_re = re.compile(' silence_end: (?P<end>[0-9]+(\.?[0-9]*)) ')
total_duration_re = re.compile('size=[^ ]+ time=(?P<hours>[0-9]{2}):(?P<minutes>[0-9]{2}):(?P<seconds>[0-9\.]{5}) bitrate=')

def get_chunk_times(audioStream, silence_threshold, silence_duration):

    p = subprocess.Popen((audioStream.filter('silencedetect', n='{}dB'.format(silence_threshold), d=silence_duration).output('-', format='null').compile()) + ['-nostats'], stderr=subprocess.PIPE)

    output = p.communicate()[1].decode('utf-8')

    if p.returncode != 0: ## shut down on error
        sys.stderr.write(output)
        sys.exit(1)

    lines = output.splitlines()

    # Chunks(Louds) start when silence ends, and chunks(Louds) end when silence starts.
    chunk_starts = []
    chunk_ends = []
    for line in lines: ## foreach line in lines
        # check the line that we are currently looking at for any start info, end info and total time info
        silence_start_match = silence_start_re.search(line) # regexpattern.search(texttobesearched)
        silence_end_match = silence_end_re.search(line)
        total_duration_match = total_duration_re.search(line)


        if silence_start_match:
            chunk_ends.append(float(silence_start_match.group('start')))
            if len(chunk_starts) == 0:
                # Started with non-silence.
                chunk_starts.append(0.)

        elif silence_end_match:
            chunk_starts.append(float(silence_end_match.group('end')))
        elif total_duration_match:
            hours = int(total_duration_match.group('hours'))
            minutes = int(total_duration_match.group('minutes'))
            seconds = float(total_duration_match.group('seconds'))
            end_time = hours * 3600 + minutes * 60 + seconds

    if len(chunk_starts) == 0:
        # No silence found.
        chunk_starts.append(0.)

    if len(chunk_starts) > len(chunk_ends):
        # Finished with non-silence.
        chunk_ends.append(10000000.)

    return list(zip(chunk_starts, chunk_ends))

import os
import errno
def _makedirs(path):
    """Python2-compatible version of ``os.makedirs(path, exist_ok=True)``."""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise

import argparse

parser = argparse.ArgumentParser(description='Arguments for tuberscutter')
parser.add_argument("-d",default=0.3, type=float, help="Value for default duration, 0.3 if you dont specify")
parser.add_argument("-t",default=-60, type=float, help="Value for default threshold, -60 db if you dont specify")
parser.add_argument("-f", default='.mp4', type=str, help="Format of the output, .mp4 if you dont specify")
parser.add_argument("--file", required=True, type=str, help="Path to your video")

args = parser.parse_args()
DEFAULT_DURATION = args.d
DEFAULT_THRESHOLD = args.t

def split_video(in_filename, out_pattern, silence_threshold=DEFAULT_THRESHOLD, silence_duration=DEFAULT_DURATION):
    originalStream = ffmpeg.input(in_filename)

    audioStream = originalStream.audio

    chunk_times = get_chunk_times(audioStream, silence_threshold, silence_duration)
    print("Chunk times are OK!")
    for i, (start_time, end_time) in enumerate(chunk_times):
        time = end_time - start_time
        if time <= 0.2:
            continue

        out_filename = out_pattern + str(i) + args.f
        #_makedirs(os.path.dirname(out_filename))
        # splitting:
        with subprocess.Popen(   (ffmpeg.input(in_filename, ss=start_time, t=time).output(out_filename).overwrite_output().compile())    ) as proc:
            proc.wait()
        print(str(i) + " out of "+ str(l) +" is done")


split_video(args.file,"L")

