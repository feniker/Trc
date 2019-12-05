from readTrc import Trc
import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.fftpack as sc
from scipy.optimize import curve_fit

Rsh = 0.025 # сопротивление шунта
MARKER_STEP = 30000
def get_num(str):
    return int(str[-6:-4])
def get_ch(str):
    return int(str[1:2])
trc = Trc()
InputDirectory = 'D:\Python\Trc\datanew'
OutputDirectory = 'D:\Python\Trc\datax'
files = os.listdir(InputDirectory)
DATX = [[[], []] for i in range(35)]
DATY = [[[], []] for i in range(35)]
for i in files:
    print(i)
    datX, datY, d = trc.open(InputDirectory+'/'+i)
    DATX[get_num(i)][get_ch(i)-1] = datX
    DATY[get_num(i)][get_ch(i)-1] = datY
# графики интегралов
def integral(x_, y_, st = 10000):
    ansy = []
    ansx = []
    for i in range(len(x_)//st):
        ansx.append(x_[i*st])
        ansy.append(np.trapz(y_[:i*st], x = x_[:i*st]))
    return (ansx, ansy)
def addPlotInt(listPl):
    xRel = []
    yRel = []
    for i in range(len(listPl)):
        print(i, type(DATX[listPl[i]][1]))
        xaxe, integ = integral(DATX[listPl[i]][1], DATY[listPl[i]][1]/5)#так как намотал 5 витков
        xRel.append(max((DATY[listPl[i]][0]))/Rsh)
        yRel.append(max(integ))
        plt.scatter(max((DATY[listPl[i]][0]))/Rsh, max(integ), c = "black", s = 3)
        #plt.plot(DATX[listPl[i]][0][::100], 0.0013*DATY[listPl[i]][0][::100]/Rsh/240, label = 'I - '+str(i))# так как F = IL/N, где I = U/Rsh
    par = np.polyfit(xRel, yRel, 1)
    lsm = np.poly1d(par)
    print("МНК для данных точек", par)
    xline = np.linspace(0.3, 300-0.3, 1000)
    yline = [lsm(i) for i in xline]
    plt.plot(xline, yline, c = "black", lw = 0.5)

addPlotInt(range(1, 35))
plt.grid(True, color = "k")
plt.ylim(0, 0.00175)
plt.xlim(0, 300)
plt.xlabel("I, A")
plt.ylabel("Ф, Вб")
plt.savefig("Flux from Current")
plt.show()