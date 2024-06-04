import subprocess, os


def convert_480p(source):
    print("this is the source:", source)
    target = source + "_480p.mp4"
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'  .format(source, target)    
    subprocess.run(cmd, shell=True)
    
def convert_720p(source):
    target = source + "_720p.mp4"
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'  .format(source, target)    
    subprocess.run(cmd, shell=True)
    
def delete_720p(source):
    target = source + "_720p.mp4"
    os.remove(target)
    
def delete_480p(source):
    target = source + "_480p.mp4"
    os.remove(target)
