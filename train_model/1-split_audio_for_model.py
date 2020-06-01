from pydub import AudioSegment
import os


GENRE = "genres"

filepath = 'absolute_path'
filename = os.listdir(filepath)
for i in range(len(filename)):
	if filename[i][-3:] == "mp3":
		song = AudioSegment.from_file(filepath + filename[i], format="mp3").set_frame_rate(22050).set_channels(1)
	elif filename[i][-3:] == "m4a":
		song = AudioSegment.from_file(filepath + filename[i], format="m4a").set_frame_rate(22050).set_channels(1)
	elif filename[i][-3:] == "wav":
		song = AudioSegment.from_file(filepath + filename[i], format="wav").set_frame_rate(22050).set_channels(1)
	split = song[00 * 1000: 30 * 1000]
	fn = filepath + GENRE + str(i) + ".wav"
	split.export(fn, format="wav")
	print("读取 / Load {} / {}".format(i + 1, len(filename)))

print("全部完成 / Finished")
