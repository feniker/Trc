from readTrc import Trc
import matplotlib.pyplot as plt
import os
import numpy as np

Rsh = 0.025 # сопротивление шунта
MARKER_STEP = 30000
def get_num(str):
    return int(str[-6:-4])
def get_ch(str):
    return int(str[1:2])
trc = Trc()
InputDirectory = 'D:\Python\Trc\Measure (2)'
files = os.listdir(InputDirectory)
DATX = [[[], [], [], []] for i in range(15)]
DATY = [[[], [], [], []] for i in range(15)]
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
def addPlot(listPl, num):
    for i in range(len(listPl)):
        print(i, type(DATX[listPl[i]][num]))
        plt.plot(DATX[listPl[i]][num][::100], DATY[listPl[i]][num][::100])
def addPlotInt(listPl):
    xRel = []
    yRel = []
    for i in range(len(listPl)):
        print(i, type(DATX[listPl[i]][1]))
        xaxe, integ = integral(DATX[listPl[i]][1], DATY[listPl[i]][1]/5)#так как намотал 5 витков
        xRel.append(max((DATY[listPl[i]][0]))/Rsh)
        yRel.append(max(integ))
        plt.scatter(max((DATY[listPl[i]][0]))/Rsh, max(integ), c = "black", s = 3)
    par = np.polyfit(xRel, yRel, 1)
    lsm = np.poly1d(par)
    print("МНК для данных точек", par)
    xline = np.linspace(0.3, 300-0.3, 1000)
    yline = [lsm(i) for i in xline]
    plt.plot(xline, yline, c = "black", lw = 0.5)
def addInt(listPl, num, ratio1 = 1, ratio2 = 1/5, color = "black", colorline = "black", colorComp = "blue"):
    xRel = []
    yRel = []
    for i in range(len(listPl)):
        print(i, type(DATX[listPl[i]][1]))
        xaxe, integ = integral(DATX[listPl[i]][num]*ratio1, DATY[listPl[i]][num]*ratio2)  # так как намотал 5 витков
        xRel.append(max((DATY[listPl[i]][0]))/Rsh)
        yRel.append(max(integ))
        plt.plot(xaxe, integ, c = 'black', lw = 0.5)
        plt.scatter(max(DATY[listPl[i]][0]) / Rsh, max(integ), c=color, s=7)
    par = np.polyfit(xRel, yRel, 1)
    lsm = np.poly1d(par)
    print("МНК для данных точек", par)
    xline = np.linspace(0.3, 200 - 0.3, 1000)
    yline = [lsm(i) for i in xline]
    plt.plot(xline, yline, c="black", lw=0.5)
    #plt.errorbar(xRel, yRel, yerr=np.array(yRel)*0.01) доделать усы


def addFlux(xList, listFlux, color = "black"):
    for i in range(len(listFlux)):
        plt.scatter(max(DATY[xList[i]][0]) / Rsh, listFlux[i]/100000, marker = "+", color = color, s = 100)


CompFlux1 = [94.3, 71.8, 82.6, 61.3, 49.9, 38.3]
CompFlux2 = [92.7, 81.3, 70.9, 59.4, 48.9, 37.4, 103.0]

addInt([1] + list(range(3, 8)), 1)
#addInt([1] + list(range(3, 8)), 2, ratio2 = 0.1, color = "blue")
#addInt([1] + list(range(3, 8)), 3, ratio2 = 0.1, color = "red")
addFlux([1] + list(range(3, 8)), CompFlux1, color = "green")
plt.grid(True, color = "k")
plt.ylim(0.0002, 0.001)
plt.xlim(50, 200)
plt.xlabel("I, A")
plt.ylabel("Ф, Вб")
plt.savefig("diamag")
plt.show()

addInt(range(8, 15), 1)
#addInt(range(8, 15), 2, ratio2 = 0.1, color = "blue")
#addInt(range(8, 15), 3, ratio2 = 0.1, color = "red")
addFlux(range(8, 15), CompFlux2, color = "green")
plt.ylim(0.0002, 0.001)
plt.xlim(50, 200)
plt.xlabel("I, A")
plt.ylabel("Ф, Вб")
plt.grid(True, color = "k")
plt.savefig("DIA1")
plt.show()