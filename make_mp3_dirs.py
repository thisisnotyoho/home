from glob import glob
from mutagen.easyid3 import EasyID3
import os
import shutil

for filename in glob('*.mp3'):
	info = EasyID3(filename)
	song = info['title'][0]
	dirname = song[0:song.index(' "')].replace(':','-')
	os.makedirs(dirname, exist_ok=True)
	shutil.move(filename, dirname + "/" + filename)
	#print("make " + dirname)
	#print("move " + filename + " to " + dirname + "/" + filename)
	

