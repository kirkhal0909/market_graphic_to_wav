from pandas_datareader import data
import datetime
import os

DATE_START = datetime.datetime(2019,1,1)
DAYS = 21
#DIVIDER = 4
DATE_END = datetime.datetime(2019,12,31)#datetime.datetime.now()

SOUNDS_FOLDER = "sounds"


freq = '''C	8,18	16,35	32,70	65,41	130,8	261,6	523,3	1047	2093	4186	8372	16744
C#	8,66	17,32	34,65	69,30	138,6	277,2	554,4	1109	2217	4435	8870	17740
D	9,18	18,35	36,71	73,42	146,8	293,7	587,3	1175	2349	4699	9397	18795
D#	9,72	19,45	38,89	77,78	155,6	311,1	622,3	1245	2489	4978	9956	19912
E	10,30	20,60	41,20	82,41	164,8	329,6	659,3	1319	2637	5274	10548	21096
F	10,91	21,83	43,65	87,31	174,6	349,2	698,5	1397	2794	5588	11175	22351
F#	11,56	23,12	46,25	92,50	185,0	370,0	740,0	1480	2960	5920	11840	23680
G	12,25	24,50	49,00	98,00	196,0	392,0	784,0	1568	3136	6272	12544	25088
G#	12,98	25,96	51,91	103,8	207,7	415,3	830,6	1661	3322	6645	13290	26580
A	13,75	27,50	55,00	110,0	220,0	440,0	880,0	1760	3520	7040	14080	28160
A#	14,57	29,14	58,27	116,5	233,1	466,2	932,3	1865	3729	7459	14917	29834
B	15,43	30,87	61,74	123,5	246,9	493,9	987,8	1976	3951	7902	15804	31609'''.replace(',','.').split('\n')

tickers = ['POLY.ME', 'PLZL.ME', 'RUAL.ME', 'VSMO.ME', 'GMKN.ME', 'MAGN.ME', 'NLMK.ME', 'CHMF.ME', 'TRMK.ME', 'ALRS.ME', 'AKRN.ME', 'PHOR.ME', 'AFLT.ME', 'BANE.ME', 'BANEP.ME', 'LKOH.ME', 'ROSN.ME', 'SNGS.ME', 'SNGSP.ME', 'TATN.ME', 'TATNP.ME', 'TRNFP.ME', 'VTBR.ME', 'CBOM.ME', 'SBER.ME', 'SBERP.ME', 'GAZP.ME', 'IRAO.ME', 'NVTK.ME', 'RSTI.ME', 'HYDR.ME', 'FEES.ME', 'UPRO.ME', 'LSRG.ME', 'PIKK.ME', 'LNTA.ME', 'MGNT.ME', 'MVID.ME', 'MTSS.ME', 'RTKMP.ME', 'RTKM.ME', 'MOEX.ME', 'NKNC.ME', 'AFKS.ME', 'GCHE.ME', 'YNDX.ME']

def getFreq(note=1,octave=1):
    if octave<1:
        octave = 1
    elif octave>12:
        octave = 12
    if note < 1:
        note = 1
    elif note > 12:
        note = 12
    note -= 1
    return float(freq[note].split('\t')[octave])

def getFreqByNote(note=1):
    octave = 1
    while note > 12:
        octave += 1
        note -= 12
    return getFreq(note,octave)

def __downloadPeriod__(ticker):    
    try:        
        period = data.DataReader(ticker, 'yahoo',DATE_START,DATE_END)
        return period
    except KeyError:        
        return None

def getNotesFromGraphic(ticker):
    period = __downloadPeriod__(ticker)
    if type(period) != type(None):
        day = 0
        means = []
        while day < len(period):
            calc_days = min(len(period)-day,DAYS)
            sm = period['Close'][day:day+calc_days].sum()
            
            means.append(sm/calc_days)
            day += calc_days
        noteStart = means[0]
        noteDiv = 10**20
        for mean in range(len(means)-1):
            pNote = abs(means[mean]-means[mean+1])
            if(pNote < noteDiv):
                noteDiv = pNote                
        notes = []

        c4 = 70
        for mean in means:
            notes.append(int(round((mean-noteStart)/noteDiv)) + c4)
        
        return notes
    else:
        return None

def soundGenerator(notes,wavName = "gen.wav"):
    rate = 44100
    duration = 0.1

    t = np.empty(0)
    x = np.empty(0)
    timesRepeat = 2
    for noteFrom in notes:
        for repeat in range(timesRepeat):#random.randint(1,2)):            
            for note in [noteFrom,noteFrom+2,noteFrom+4,noteFrom+6,noteFrom+4,noteFrom+2,noteFrom]: #arp
                frequency = getFreqByNote(note)
                tAp = np.linspace(0, duration, duration*rate, endpoint=False)        
                t = np.append(t,tAp)     
                xAp = np.sin(2*np.pi * frequency * tAp)
                x = np.append(x,xAp)
    wavio.write(wavName, x, rate, sampwidth=3)

def tickerToWav(ticker):
    if not os.path.exists(SOUNDS_FOLDER):
        os.mkdir(SOUNDS_FOLDER)
    
    soundGenerator(getNotesFromGraphic(ticker),SOUNDS_FOLDER+'/'+ticker+'.wav')
    print(ticker,'- wav generated!')






import numpy as np
import wavio
import math
import random

#F=Round(440*Exp(Ln(2)*(No-(10-Nn)/12)))
for ticker in tickers:
    tickerToWav(ticker)

