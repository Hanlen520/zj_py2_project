# -*- coding: utf-8 -*-
'''
Created on 2014-11-7

@author: zhengjin
'''

import os

class DoParseFrames:
    def __init__(self, inPath, outPath):
        self.inPath = inPath
        self.outPath = outPath
        self.parseItems = []
        self.stdPercent = 0.1
        
    def DoParse(self, trace):
        tag = "trace_frame"
        time = trace[6:14]
        frames = trace[trace.index(tag) + len(tag) + 2: ]
        
        self.parseItems.append((time, frames))
        
    def DumpParse(self, fout):
        subIndex = int(round(len(self.parseItems) * self.stdPercent))
        total = 0
        
        for item in sorted(self.parseItems, key = lambda item : float(item[1]))[0 : subIndex]:
            total += float(item[1])
            fout.write('%s,frame rate: ,%s\n' %(item[0], item[1]))
#             print('%s,frame rate: ,%s' %(item[0], item[1]))

        fout.write("N/A,Average: ,%f\n" %(total/subIndex))
#         print("N/A,average frames: ,%f" %(total/count))

    def ParseFrames(self):
        patn = "trace_frame:"
        fin = open(self.inPath, 'r')
    
        if os.path.exists(self.outPath):
            os.remove(self.outPath)
        fout = open(self.outPath, 'a')
    
        lines = fin.readlines()
        for line in lines:
            if line.find(patn) > 0:
                    self.DoParse(line.strip('\n'))
        
        self.DumpParse(fout)
        
        fin.close()
        fout.close()
    

if __name__ == '__main__':
    inPath = r"D:\Launcher_KeyTarget\FramesLog_08_AppSubMenuList.log"
    outPath = r"D:\Launcher_KeyTarget\FramesLog_08_AppSubMenuList_Parse1.log"
        
#         Parse("11-07 16:23:42.150 D/cocos2d-x debug info(18418): trace_frame: 41.617416", input)
#         FileFilter(input, output)

    DoParseFrames(inPath, outPath).ParseFrames()
    print("Frames parse done!")
    pass
