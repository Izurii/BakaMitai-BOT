import os, sys, subprocess, io, time, random, hashlib
import requests, json, mimetypes
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
from mhmovie.code import *

#Sys argvs
source_image_url = sys.argv[1]

#Files needed
source_image = '../bakamitai/images/'
driving_video = '../bakamitai/bakamitai_video_template.mp4'
audio = 'bakamitai_audio.wav'
configFile = 'config/vox-256.yaml'

#Vars for deepfake script
resultPath = '../bakamitai/videos/result.mp4'

#Vars for internal use of script bakamitai
actualDir = os.path.abspath(os.getcwd())+'/'
videoBakamitai = actualDir+'/videos/result.mp4'
audioBakamitai = actualDir+'/bakamitai_audio.wav'
finalVideoPath = actualDir+'/videos/final_result.mp4'
dateString = datetime.today().strftime('%Y-%m-%d')

#Save of stdout and stderr
temp_stdout = sys.stdout
temp_stderr = sys.stderr

#Logs files
#logFile = normal log
#errFile = warn/error logs
deepFakeLogsDir = actualDir+'deepfake_logs/'
deepFakeLogFile = open(deepFakeLogsDir+'logfile '+dateString+'.txt', 'a') 
deepFakeErrFile = open(deepFakeLogsDir+'errfile '+dateString+'.txt', 'a') 

bakaMitaiLogsDir = actualDir+'bakamitai_logs/'
bakaMitaiLogFile = open(bakaMitaiLogsDir+'logfile.txt '+dateString+'', 'a') 
bakaMitaiErrFile = open(bakaMitaiLogsDir+'errfile.txt '+dateString+'', 'a') 

def makeBakamitaiVideo():
	
	sp_bakamitai_video = Popen(
		'py demo.py'
		+ ' --source_image ' + source_image
		+ ' --driving_video ' + driving_video
		+ ' --result_video ' + resultPath
		+ ' --config ' + configFile,
		cwd='../deepfake/',
		stdout=deepFakeLogFile,
		stderr=deepFakeErrFile
		)

	# for line in sp_bakamitai_video.stdout:
	# 	line = line.decode('utf-8')
	# 	deepFakeLogFile.write(line)

	# for line in sp_bakamitai_video.stderr:
	# 	line = line.decode('utf-8')
	# 	deepFakeErrFile.write(line)

	sp_bakamitai_video.wait()

def putAudioBakaMitai(video, audio, output):
	
	if not os.path.exists(videoBakamitai):
		error_deepfake(e)

	command = "ffmpeg -i {video} -i {audio} -c:v copy -c:a aac {output}".format(video=video, audio=audio, output=output)
	sp_bakamitai_audio = Popen(command, stdout=bakaMitaiLogFile, stderr=bakaMitaiErrFile)

	# for line_out in sp_bakamitai_audio.stdout:
	# 	line_out = line_out.decode('utf-8')
	# 	bakaMitaiLogFile.write(line_out)

	# for line_err in sp_bakamitai_audio.stderr:
	# 	line_err = line_err.decode('utf-8')
	# 	bakaMitaiErrFile.write(line_err)

	sp_bakamitai_audio.wait()

def download_file(url):
	filename_temp = str(time.time())+str(random.randint(0, 999999))
	filename = hashlib.sha224(filename_temp.encode('utf-8')).hexdigest()
	mimetypes_allowed = ['.jpg', '.png', '.jpeg']
	try:
		response = requests.get(url)
		content_type = response.headers['content-type']
		extension = mimetypes.guess_extension(content_type)

		if extension.lower() == ".jpe":
			extension = ".jpg"

		if extension.lower() not in mimetypes_allowed:
			error_extension()

		file = open(actualDir+'images/'+filename+extension, "wb")
		file.write(response.content)
		file.close()
		return (filename+extension)
	except Exception as e:
		error_download(e)

def error_deepfake(e):
	deepFakeErrFile.write("Error: " + e)
	print('error_deepfake')
	exit()

def error_bakamitai(e):
	bakaMitaiErrFile.write("Error: " + e)
	print('error_bakamitai')
	exit()

def error_download(e):
	bakaMitaiErrFile.write("Error: " + e)
	print('error_download')
	exit()

def error_extension():
	bakaMitaiErrFile.write("Error: " + e)
	print('error_file_format')
	exit()

try:
	source_image += download_file(source_image_url)
	makeBakamitaiVideo()
	try:
		putAudioBakaMitai(videoBakamitai, audioBakamitai, finalVideoPath)
		os.remove(videoBakamitai)
		print(finalVideoPath)
	except Exception as e:
		error_bakamitai(e)
except Exception as e:
	error_deepfake(e)