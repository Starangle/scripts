''' 
支持wav文件
该脚本可以从一段wav文件中以秒单位截取一部分音频，默认截取120秒，如果音乐不足120秒
则全部保留。

基本用法如下：
WavCut inputWav outputWav
inputWav是源文件，outputWav是输出文件，如果该文件存在，则会被覆盖。

此外可以通过-b参数指定要开始截取的位置(以秒计算，必须为整数)，-e参数可以指定截取的
结束位置(以秒计算，必须为整数)。若仅指定-b则截取[begin_time,begin_time+120)区间内
的音频，若仅指定-e则截取[0,end_time)区间的内容。如果end_time超出音频总时间，则只截
取到音频末尾，不会补充空白。

'''

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
		return -1

	try:
		in_file=wave.open(in_name,'rb')
	except:
		sys.stderr.write("no such input file")
		return -2
	finally:
		pass

	params=in_file.getparams()

	global simple_rate
	simple_rate=params.framerate

	begin_frame=sec2frame(begin_time)
	end_frame=sec2frame(end_time)

	if begin_frame>params.nframes:
		sys.stderr.write("the begin time beyond the total length of wav")
		return -3

	in_file.setpos(begin_frame)
	data=in_file.readframes(end_frame-begin_frame)

	params._replace(nframes=end_frame-begin_frame)
	out_file=wave.open(out_name,'wb')
	out_file.setparams(params)
	out_file.writeframes(data)

	in_file.close()
	out_file.close()
	return 0

if __name__ == '__main__':

	begin_time=0
	end_time=120
	
	try:
		opts,args=getopt.getopt(sys.argv[1:],"b:e:",[])
	except:
		sys.stderr.write("can not parse the params")
		exit(0)
	finally:
		pass

	if len(args)!=2:
		print("usage: WavCut inputWav outputWav")
		exit(0)
	else:
		in_name=args[0]
		out_name=args[1]

	for opt,val in opts:
		if opt == '-b':
			begin_time=int(val)
			end_time=begin_time+120
		elif opt=='-e':
			end_time=int(val)

	statu=main(in_name,out_name,begin_time,end_time)
	exit(statu)
