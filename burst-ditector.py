#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
burst ditector
"""
import wave
import numpy as np
import scipy.fftpack

from numpy import frombuffer


class BurstDitector(object):
    """
    burst ditector
    """
    def __init__(self):
        pass

    def is_burst(self, path):
        """
        burst
        path: wave file path
        """
        # FFTをするwaveファイルを開く
        wf = wave.open(path, 'r')
        sampling_rate = wf.getframerate()   # サンプリング周波数の取得
        audioframe = wf.readframes(sampling_rate)   # fps
        bit_rate = frombuffer(audioframe, dtype="int16") / 32768.0
        wf.close()

        START = 0     # サンプリングする開始位置
        FFT_SAMPLE = 2048   # FFTのサンプル数

        # ビットレートの1次元配列をFFT変換した時の解を取得する
        fft_result = scipy.fftpack.fft(bit_rate[START:START + FFT_SAMPLE])

        # サンプリング周波数を取得する (?
        freqlist = np.fft.fftfreq(FFT_SAMPLE, d=1.0 / sampling_rate)

        # 周波数スペクトルの値を取得して対数に変換
        adft = np.abs(fft_result)
        adft_log = 20 * np.log10(adft)

        # パワースペクトルの値を取得して対数に変換
        pdft = np.abs(fft_result)
        pdft_log = 10 * np.log10(pdft)
    
        # ケプストラム分析
        acps = np.real(np.fft.ifft((adft_log))) # 振幅スペクトル
        pcps = np.real(np.fft.ifft((pdft_log))) # パワースペクトル

        # ケプストラム次数
        cepcoef = 20
        acpslif = np.array(acps)    # 振幅スペクトル
        pcpslif = np.array(pcps)    # パワースペクトル

        # 高周波数成分を除去
        acpslif[cepcoef:len(acpslif) - cepcoef + 1] = 0 # 振幅スペクトル
        pcpslif[cepcoef:len(pcpslif) - cepcoef + 1] = 0 # パワースペクトル

        # ケプストラムをフーリエ変換しなおしてスペクトルに変換し直す
        adftspc = np.fft.fft(acpslif, FFT_SAMPLE)   # 振幅スペクトル
        pdftspc = np.fft.fft(pcpslif, FFT_SAMPLE)   # パワースペクトル

        # ケプストラム分析の近似直線
        x = freqlist[0:FFT_SAMPLE / 2]
        y = pdftspc[0:FFT_SAMPLE / 2]

        a = np.array([x, np.ones(len(x))])
        a = a.T
        a, b = np.linalg.lstsq(a, y)[0]

        # 傾きの値をわかりやすい数値に変換
        a = float(a)
        a = a * 10000

        if abs(a) > 4.58:
            return False
        else:
            print True


if __name__ == '__main__':
    path = raw_input("testing file>")
    b = BurstDitector()
    if b.is_burst(path):
        print "Normal"
    else:
        print "Angry"

