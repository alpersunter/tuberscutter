import os
import errno
def _makedirs(path):
    """Python2-compatible version of ``os.makedirs(path, exist_ok=True)``."""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise


DEFAULT_DURATION = 0.3
DEFAULT_THRESHOLD = -60

def split_video(in_filename, out_pattern, silence_threshold=DEFAULT_THRESHOLD, silence_duration=DEFAULT_DURATION):
    originalStream = ffmpeg.input(in_filename)

    audioStream = originalStream.audio

    chunk_times = get_chunk_times(audioStream, silence_threshold, silence_duration)

    for i, (start_time, end_time) in enumerate(chunk_times):
        time = end_time - start_time
        out_filename = out_pattern + str(i)
        _makedirs(os.path.dirname(out_filename))
        # splitting:
        subprocess.Popen(   (ffmpeg.input(in_filename, ss=start_time, t=time).output(out_filename).overwrite_output().compile())    )

