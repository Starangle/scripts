# 计算wav的短时能量特征,仅支持PCM编码的wav
# 接受一个参数，指定wav文件路径
import matplotlib.pyplot as plt
import numpy as np
import sys
import wave

'''
计算公式x(i,j)=wav(i+j)*window(j) (j=0:fl-1)
E(i)=sum(x(i,j)**2) (j=0:fl-1,i=0:fs:wavLen)
'''


def st_energy(wav:'单通道PCM编码波形序列',
             window:'窗函数序列', 
             fs:'帧移'):

    fl = len(window)        #帧长
    wavLen = len(wav)       #波形序列长度
    n = int(len(wav) / fs)  #帧数
    e = np.zeros(n)         #短时能量序列
    print(wavLen)
    for i in range(n):
        ti = i * fs         #第i帧的起始下标fullname:true_i
        for j in range(fl):
            v1 = 0 if ti + j >= wavLen else wav[ti + j]
            v2 = v1 * window[j]
            e[i] += v2 ** 2
    return e


if __name__ == '__main__':
    name = sys.argv[1]
    try:
        hWav = wave.open(name, 'r')
    except FileExistsError:
        sys.stderr.write("no such file : %s" % (name))
    params = hWav.getparams()
    strWav = hWav.readframes(params.nframes)
    
    type = np.int16 if params.sampwidth == 2 else np.int8
    arrWav = np.fromstring(strWav,type)
    arrWav = np.reshape(arrWav,[-1,params.nchannels])
    arrWav = arrWav.T

    windowLen = 40      #这里修改帧长
    fs = 20             #这里修改帧移

    x1 = [i / params.framerate for i in range(params.nframes)]
    x2 = [i for i in range(int(params.nframes / fs))]
    fea = st_energy(arrWav[0],np.hamming(windowLen), fs)
    plt.subplot(211)
    plt.xlabel('Time/s')
    plt.ylabel('Amp')
    plt.plot(x1,arrWav[0])
    plt.subplot(212)
    plt.xlabel('N')
    plt.ylabel('Energy')
    plt.plot(x2,fea)
    plt.show()

