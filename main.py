from readTrc import Trc
import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.fftpack as sc
from scipy.optimize import curve_fit

Rsh = 0.025 # сопротивление шунта
MARKER_STEP = 30000
def funcCh1(x, w, A1, phi):
    return A1*np.sin(w*x + phi)
#def T_max(y):
#    return y.find(max(y))
def get_num(str):
    return int(str[-6:-4])
def get_ch(str):
    return int(str[1:2])
trc = Trc()
InputDirectory = 'D:\Python\Trc\data'
OutputDirectory = 'D:\Python\Trc\datax'
files = os.listdir(InputDirectory)
DATX = [[[], [], []] for i in range(19)]
DATY = [[[], [], []] for i in range(19)]
for i in files:
    print(i)
    datX, datY, d = trc.open(InputDirectory+'/'+i)
    DATX[get_num(i)][get_ch(i)-1] = datX
    DATY[get_num(i)][get_ch(i)-1] = datY
    #if (i[0:2] == "C1"):
    #    plt.plot(datX, datY/0.025, lw = 0.5, c = 'black')
    #else:
    #    plt.plot(datX[::10], datY[::10]/0.025, lw = 0.5, c = 'black')
    """
    if i == "C1--Trace--00001.trc":
        plt.scatter(datX[T_max(datY)], datY[T_max(datY)])
        plt.show()
        newDataX = np.where(datX<0, 0, datX)
        newDataY = np.where(datX<0, 0, datY)
        par, buf = curve_fit(funcCh1, datX[::10], -datY[::10])
        print(par)
        plt.plot(datX[::100], -datY[::100], lw = 0.5, c = 'black')
        plt.plot(datX[::100], funcCh1(datX[::100], *par))
        plt.plot(newDataX[::100], -newDataY[::100])
        plt.show()
        #spectrum = sc.rfft(datY[::10])
        #plt.plot(sc.rfftfreq(len(datX[::10]), datX[10]-datX[0]), np.abs(spectrum)/len(datX[::10]))
        #plt.show()
    """
    #plt.savefig(OutputDirectory+'/'+i[0:-4]+'.png')
    #plt.close()

    """
    dat = [str(datX), str(datY)]
    with open(OutputDirectory+'/'+i[0:-4]+'.txt', 'w') as out:
        out.writelines(''.join(str(datX)))
        out.writelines(''.join(str(datY)))
    """
for i in range(7,19):
    if not DATX[i][0] == []:
        plt.plot(DATX[i][0][::100], np.abs(DATY[i][0][::100]/0.025), lw = 0.5, label = str(i))
        print("(Ch", i, 0, ") is added")
plt.legend()
plt.show()
#графики первого канала
"""
plt.plot(DATX[18][0][::100], DATY[18][0][::100]/0.025, lw = 0.25, label = "0 вит.", c = 'black')
plt.plot(DATX[9][0][::100], DATY[9][0][::100]/0.025, lw = 0.25, label = "30 вит.", c = 'black')
plt.scatter(DATX[9][0][::MARKER_STEP], DATY[9][0][::MARKER_STEP]/0.025, c = 'black', marker = "X", lw = 0.025)
plt.plot(DATX[15][0][::100], DATY[15][0][::100]/0.025, lw = 0.25, label = "80 вит.", c = 'black')
plt.scatter(DATX[15][0][::MARKER_STEP], DATY[15][0][::MARKER_STEP]/0.025, c = 'black', marker = "^", lw = 0.025)
plt.plot(DATX[13][0][::100], DATY[13][0][::100]/0.025, lw = 0.25, label = "100 вит.", c = 'black')
plt.scatter(DATX[13][0][::MARKER_STEP], DATY[13][0][::MARKER_STEP]/0.025, c = 'black', marker = "v", lw = 0.025)
plt.legend()
plt.show()
"""
# графики второго минус третьего каналов

AbsMax = np.amax(np.abs(DATY[16][0]))

for i in range(9,19):
    if not (DATX[i][1] == [] or DATX[i][2] == []):
        l= len(DATX[i][1])
        ratio = AbsMax/np.amax(np.abs(DATY[i][0]))
        plt.plot(DATX[i][1][:l//2:100], (DATY[i][1][:l//2:100] - DATY[i][2][:l//2:100])*ratio, lw = 0.5, label = str(i))
        print("(Ch", i, 0, ") is added")
plt.legend()
plt.show()

def plot(num_, l_, ratio_, color_, marker_ = None):
    plt.plot(DATX[num_][1][:l_ // 2:100], (DATY[num_][1][:l_ // 2:100] - DATY[num_][2][:l // 2:100]) * ratio_, lw=0.5, c=color_)
    if marker_ is not None:
        plt.scatter(DATX[num_][1][:l_ // 2:MARKER_STEP],
                    (DATY[num_][1][:l_ // 2:MARKER_STEP] - DATY[num_][2][:l_ // 2:MARKER_STEP]) * ratio_,
                    c=color_, marker = marker_, s=20, linewidths=0.5)
    else:
        plt.scatter(DATX[num_][1][:l_ // 2:MARKER_STEP],
                    (DATY[num_][1][:l_ // 2:MARKER_STEP] - DATY[num_][2][:l_ // 2:MARKER_STEP]) * ratio_,
                    c=color_, s=20, linewidths=0.5)
def addPlot(listPl, listMk):
    for i in range(len(listPl)):
        l = len(DATX[listPl[i]][1])
        ratio = AbsMax / np.amax(np.abs(DATY[listPl[i]][0]))
        plot(listPl[i], l, ratio, 'black', marker_=listMk[i])

def integral(x_, y_, st = 10000):
    ansy = []
    ansx = []
    for i in range(len(x_)//st):
        ansx.append(x_[i*st])
        ansy.append(np.trapz(y_[:i*st], x = x_[:i*st]))
    return (ansx, ansy)
def addPlotInt(listPl):
    for i in range(len(listPl)):
        ratio = AbsMax / np.amax(np.abs(DATY[listPl[i]][0]))
        print(i, type(DATX[listPl[i]][1]))
        xaxe, integ = integral(DATX[listPl[i]][1], ratio*DATY[listPl[i]][1]/10)#так как в основной петле комепнсатора 10 витков
        plt.plot(xaxe, integ, label = str(i))
        plt.plot(DATX[listPl[i]][0][::100], ratio*0.0013*DATY[listPl[i]][0][::100]/Rsh/240, label = 'I - '+str(i))# так как F = IL/N, где I = U/Rsh
def FluxRelCur(listL, listFl):
    plt.plot(listL/Rsh, listFl/628/5)#т.к. витков 5 было намотано
    plt.scatter(listL/Rsh, listFl/628/5)
    plt.plot(listL/Rsh, 0.0013*listL/Rsh/240)#т.к. витков 5 было намотано
    plt.scatter(listL/Rsh, 0.0013*listL/Rsh/240)
    plt.show()

ar_I_L = np.array([7, 6.3, 5.9, 5.3, 5.06, 4.58, 4.16, 3.66, 3.29, 2.883, 2.34, 1.83, 1.312])
ar_I_fl = np.array([6.3, 5.68, 5.3, 4.82, 4.57, 4.14, 3.81, 3.35, 2.895, 2.5, 2.08, 1.65, 1.146])
FluxRelCur(ar_I_L, ar_I_fl)

addPlot([10, 12, 15, 13], [None, "*", "v", "s"])
plt.grid()
plt.xlabel("T, мс")
plt.ylabel("U, В")
plt.show()

addPlotInt([10, 12, 15, 13])
plt.grid()
plt.legend()
plt.show()



