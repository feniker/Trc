from readTrc import Trc
import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.fftpack as sc
from scipy.optimize import curve_fit
def funcCh1(x, w, A1, phi):
    return A1*np.sin(w*x + phi)
def T_max(y):
    return y.find(max(y))
trc = Trc()
InputDirectory = 'D:\Python\Trc\data'
OutputDirectory = 'D:\Python\Trc\datax'
files = os.listdir(InputDirectory)
for i in files:
    print(i)
    datX, datY, d = trc.open(InputDirectory+'/'+i)
    if (i[0:2] == "C1"):
        plt.plot(datX, -datY, lw = 0.5, c = 'black')
    else:
        plt.plot(datX[::10], datY[::10], lw = 0.5, c = 'black')
    if i == "C1--Trace--00001.trc":
        plt.scatter(datX[T_max(datY)], datY[T_max(datY)])
        plt.show()
        """
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
    plt.savefig(OutputDirectory+'/'+i[0:-4]+'.png')
    plt.close()

    """
    dat = [str(datX), str(datY)]
    with open(OutputDirectory+'/'+i[0:-4]+'.txt', 'w') as out:
        out.writelines(''.join(str(datX)))
        out.writelines(''.join(str(datY)))
    """