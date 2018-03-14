# 支持mp3

import sys,getopt
import wave

def frame2sec(n):
	global simple_rate
	return n/simple_rate

def sec2frame(s):
	global simple_rate
	return s*simple_rate

def main(in_name,out_name,begin_time,end_time):

	if begin_time>=end_time:
		sys.stderr.write("begin_time must less than end_time")
		return -2

	try:
		in_file=wave.open(in_name,'rb')
	except:
		sys.stderr.write("no such input file")
		return -3
	finally:
		pass

	params=in_file.getparams()

	global simple_rate=params.framerate

	begin_frame=sec2frame(begin_time)
	end_frame=sec2frame(end_frame)

	if begin_time>info.frame_count:
		sys.stderr.write("the begin time beyond the total length of wav")
		return -4

	in_file.setpos(begin_frame)
	data=in_file.readframes(end_frame-begin_frame)

	params.nframes=end_frame-begin_frame
	out_file=wave.open(out_name,'wb')
	out_file.setparams(params)
	out_file.writeframes(data)

	in_file.close()
	out_file.close()

if __name__ == '__main__':

	begin_time=0
	end_time=120
	
	try:
		opts,args=getopt.getopt(sys.argv,"b:e:")
	except:
		print("WavCut -i inputWav -o outputWav")
	finally:
		pass

	if len(args)!=3:
		print("WavCut -i inputWav -o outputWav")
		return -1
	else:
		in_name=args[1]
		out_name=args[2]

	for opt,val in opts:
		if opt == '-b':
			begin_time=val
			end_time=val+120
		elif opt=='-e':
			end_time=val

	return main(in_name,out_name,begin_time,end_time)