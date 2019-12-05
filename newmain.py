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
for i in range(len(DATX)):
    if not DATX[i][0] == []:
        plt.plot(DATX[i][0][::100], np.abs(DATY[i][0][::100]/0.025), lw = 0.5, label = str(i))
        print("(Ch", i, 0, ") is added")
plt.legend()
plt.show()
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
        print(max((DATY[listPl[i]][0]))/Rsh, max(integ))
        plt.scatter(max((DATY[listPl[i]][0]))/Rsh, max(integ))
        #plt.plot(DATX[listPl[i]][0][::100], 0.0013*DATY[listPl[i]][0][::100]/Rsh/240, label = 'I - '+str(i))# так как F = IL/N, где I = U/Rsh
    plt.plot(xRel, yRel)
def FluxRelCur(listL, listFl):
    plt.plot(listL/Rsh, listFl/628/5)#т.к. витков 5 было намотано
    plt.scatter(listL/Rsh, listFl/628/5)
    plt.show()


"""
ar_I_L = np.array([7, 6.3, 5.9, 5.3, 5.06, 4.58, 4.16, 3.66, 3.29, 2.883, 2.34, 1.83, 1.312])
ar_I_fl = np.array([6.3, 5.68, 5.3, 4.82, 4.57, 4.14, 3.81, 3.35, 2.895, 2.5, 2.08, 1.65, 1.146])
FluxRelCur(ar_I_L, ar_I_fl)

addPlot([10, 12, 15, 13], [None, "*", "v", "s"])
plt.grid()
plt.xlabel("T, мс")
plt.ylabel("U, В")
plt.show()
"""
addPlotInt(range(1, 35))
plt.grid()
plt.legend()
plt.savefig("Flux from Current")
plt.show()