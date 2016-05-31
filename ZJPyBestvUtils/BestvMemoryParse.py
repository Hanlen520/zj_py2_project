#!/usr/bin/python
from __future__ import division
# import sys
from pylab import *
import os

class Mem():
    def __init__(self, src):
        self.size = int(src[1].split()[1])
        self.rss = int(src[2].split()[1])
        self.pss = int(src[3].split()[1])
        self.shared_clean = int(src[4].split()[1])
        self.shared_dirty = int(src[5].split()[1])
        self.private_clean = int(src[6].split()[1])
        self.private_dirty = int(src[7].split()[1])
        self.referenced = int(src[8].split()[1])
        self.anon = int(src[9].split()[1])
        self.anonHuge = int(src[10].split()[1])
        self.swap = int(src[11].split()[1])
        self.kernel = int(src[12].split()[1])
        self.mmu = int(src[13].split()[1])
        self.locked = int(src[14].split()[1])

        self.title = src[0].strip().split()
        if len(self.title) == 6:
            self.name = self.title[5]
        else:
            self.name = "anon"

        if self.pss != 0:
            self.size = self.pss
        else:
            self.size = self.rss

class DoParseMem():
    def __init__(self):
        self.total = 0
        self.results = {}
    
    def addMem(self, mem):
        self.total += mem.size
        
        exist = self.results.get(mem.name)
        if exist == None:
            self.results[mem.name] = mem.size  # add new
        else:
            self.results[mem.name] = exist + mem.size  # for same pgm
        
    def dumpMem(self, fout):
        fout.write('Total,%s\n' %self.total)
#         print('Total,%s' %self.total)
    
        for item in sorted(self.results, key=self.results.get, reverse=True):
            if (self.results[item] > 100):
#                 print('%s,%sKb' %(item, results[item]))
#                 print('%s,%s,%.4f' %(item, self.results[item], (self.results[item] / self.total)))
                fout.write('%s,%s,%.4f\n' %(item, self.results[item], (self.results[item] / self.total)))
        
    def dumpChart(self):
        figure(1, figsize=(6,6))
    #     ax = axes([0.1, 0.1, 0.8, 0.8])
    #     first = 0
    
        i = 0
        pgms = []
        sizes = []
        top = 0
        for key in sorted(self.results, key=self.results.get, reverse=True):  # get first 5 max sizes
            sizes.append(self.results[key])
            top += self.results[key]
     
            index = key.rfind('/')  # get last word
            if index != -1 and index != 0:
                key = key[index + 1: ]
            pgms.append(key)
     
            i += 1
            if i > 4:
                break;
        # end for
    
        labels = ["%s(%d Kb)"%(pgms[0], sizes[0]), "%s(%d Kb)"%(pgms[1], sizes[1]), "%s(%d Kb)"%(pgms[2], sizes[2]), 
                  "%s(%d Kb)"%(pgms[3], sizes[3]), "%s(%d Kb)"%(pgms[4], sizes[4]), "other"]
        fracs = [sizes[0], sizes[1], sizes[2], sizes[3], sizes[4], (self.total - top)]
        explode = (0, 0.05, 0, 0, 0, 0)
        pie(fracs, labels=labels, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
        title('Total size:%d Kb' %self.total, bbox={'facecolor':'0.8', 'pad':5})
    
        show()
    
def ParseMem(logPath, newLogPath):
    fin = open(logPath, 'r')
    lines = fin.readlines()
    num = len(lines)
    
    if os.path.exists(newLogPath):
        os.remove(newLogPath)
    fout = open(newLogPath, 'w')

    i = 0
    mems = []
    while i < num:
        mems.append(Mem(lines[i:(i + 15)]))
        i += 15

    parse = DoParseMem()
    for mem in mems:
        parse.addMem(mem)

    parse.dumpMem(fout)
    
    fin.close()
    fout.close()


if __name__ == '__main__':
#    f = open(sys.argv[1])

#     dumpChart()

#     ParseMem(r"D:\Launcher_KeyTarget\MemSmaps3.log", r"D:\Launcher_KeyTarget\MemSmaps3_parse.log");
    
    print("Memory parse Done!")
    pass
