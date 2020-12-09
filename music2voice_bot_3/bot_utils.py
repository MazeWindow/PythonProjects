import pydub
import requests
import config
import os




def tg_download_music(link):
    url = config.SERVER_FILES_DIR + link  # url to download file from consists of path to server and path on server
    local_name = config.LOCAL_MP3_DIR + cut_path(link)  # cutting path, getting file name
    download_file(url, local_name)  # downloading file from url into local "music/" dir
    return local_name

def download_file(link, filename=""):
    try:
        if filename:
            pass
        else:
            req = requests.get(link)
            filename = req.url[link.rfind("/") + 1:]

        with requests.get(link) as req:
            with open(filename, "wb") as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None

def writefile(filename, data):
    try:
        with open(filename, "wb") as f:
            f.write(data)
            print("file saved")
    except Exception as e:
        print(e)
        return None

def readfile(filename):
    data=None
    try:
        with open(filename, "rb") as f:
            data=f.read()
            print("file read")
            return data
    except Exception as e:
        print(e)
        return None

def cut_path(path):
    return path[path.rfind("/") + 1:]

def cut_extension(name):
    return name[:name.rfind(".")]

def get_extension(name):
    return name[name.rfind(".")+1:]

def get_timecodes(string):
    delimiters=config.TIMING_DELIMITERS_ROAM
    for didx in range(len(delimiters)):
        for sidx in range(len(string)):
            if string[sidx] == delimiters[didx]:
                string = string.replace(string[sidx], " ")

    string = string.split(" ")
    string[0]=str2sec(string[0])
    string[-1]=str2sec(string[-1])
    return string[0], string[-1]

def str2sec(time):
    mins = int(time.split(":")[0])
    millisecs = time.split(":")[1]
    if "." in time:
        secs = int(millisecs.split(".")[0])
        millis = int(millisecs.split(".")[1])
    else:
        secs = int(millisecs)
        millis = 0
    print(mins, secs, millis)
    total = (mins * 60 + secs) * 1000 + millis
    return total

def convert_sound(timing_start, timing_end, music_file):
    print("converter running")
    print("    converting...", end=" ")
    sound=pydub.AudioSegment.from_file(config.LOCAL_MP3_DIR+music_file, format=get_extension(music_file))
    timing_start_millis = timing_start
    timing_end_millis = timing_end
    sound=sound[timing_start_millis:timing_end_millis]
    print("converted")
    print("    saving...")
    save_name=config.LOCAL_OPUS_DIR+cut_extension(music_file)+".ogg"
    print("    save path: ", save_name)
    sound.export(save_name, format="opus")
    print("    saved successfully")
    print("    deleting mp3...", end=" ")
    os.remove(config.LOCAL_MP3_DIR+music_file)
    print("    deleted successfully")
    print("    converter returning...", end=" ")
    return save_name