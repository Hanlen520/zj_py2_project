# -*- coding: utf-8 -*-
# import sys
import os

def usage():
    print("Arg error: parse only accept one arg, filename");

class Entry():
    def __init__(self, tup):
        self.obj, self.state, self.sec, self.usec = tup.split()  # split each line into 4 fields
        self.sec = int(self.sec)
        self.usec = int(self.usec)
        self.children = [] # save sub modules
        
    def addChild(self, c):
        self.children.append(c)

    def cal(self, sec, usec):
        self.latency = (sec - self.sec) * 1000 + (usec - self.usec) / 1000.0

class Parser():
    def __init__(self, content):
        self.newline = '\n'
        self.entries = []  # Entry objects
        self.stack = []  # temp cached entries
        self.outstack = []  # for output
        self.invalidstack = []  # invalid entries

        for line in content:  # read each line for input
            record = self.strip(line[1])  # format line
            if record != "":
                self.push(line[0], Entry(record))
    
    def push(self, linenum, entry):
        if entry.state == "enter":  # add function enter into stack
            if len(self.stack) == 0 or ((entry.obj == '(anon)') or (len(self.stack) > 0 and entry.obj != self.stack[-1].obj)):
            # fix cascade issue except (anon)
                self.stack.append(entry)
        elif entry.state == "exit":  # match function exit
            try:
                enter = self.stack.pop()
            except IndexError:
                print('linenum -> %d' %linenum)  # print linenum for error entry
                print("At the end of enter entries for -> %s exit function! " %(entry.obj))
                exit()
            
            if (enter.obj != entry.obj):  # fix issue, function has enter, but not exit
                enter.obj += "&nbsp;NO_EXIT"
                enter.latency = 0
                children = enter.children
                enter.children = []
                self.invalidstack.append(enter)
                
                enter = self.stack.pop()
                enter.children = children

            if (enter.obj == entry.obj):
                enter.cal(entry.sec, entry.usec)  # calculate latency
                if len(self.stack) != 0:
                    self.stack[-1].addChild(enter) # add as sub module
                else:
                    self.outstack.append(enter);
            else:  # issue, has exit, but no enter
                print('linenum -> %d' %linenum)
                print("Unexpected unmatched function entries: enter -> %s, exit-> %s" %(enter.obj, entry.obj))
                exit()
        else:
            print('linenum -> %d' %linenum)
            print("Entry -> %s not contains keyword 'enter' or 'exit'!" %(entry.obj))
            exit()
            
    def strip(self, line):
        patn = " TRACE:"
        idx = line.find(patn)
        if idx == -1:
            return ""
        return line[idx + len(patn):]
    
    def dump(self, path): # build html report
        f = open(path, 'a')
        f.write('<html><body>' + self.newline)
        
        for entry in self.outstack:
            self.dumpTree(f, entry, 0)
        f.write('<p/>' + self.newline)
        for entry in self.invalidstack:
            self.dumpTree(f, entry, 0)
        
        f.write('</body></html>' + self.newline)
        f.close()
        
    def dumpTree(self, f, entry, indent):
        #leading = "\t" * indent;
        space = "&nbsp;" * 8
        f.write('<div level="%d"' %(indent))

        self.setColor(f, entry)
        f.write("%s%s %.3f \n" % (space * indent, entry.obj, entry.latency))
        f.write("</div>" + self.newline)

        for child in entry.children:
            self.dumpTree(f, child, indent + 1)
    
    def setColor(self, f, node):
        if(node.latency >= 16 and node.latency < 80):
            f.write(' style="color:blue">' + self.newline)
        elif(node.latency >= 80 and node.latency < 160):
            f.write(' style="color:brown">' + self.newline)
        elif(node.latency > 160 or node.obj.endswith("NO_EXIT") or node.obj.endswith("NO_ENTER")):
            f.write(' style="color:red">' + self.newline)
        else:
            f.write('>' + self.newline)

class fileUtil():
    def __init__(self, path):
        self.path = path
        
    def fileFilter(self):
        patn = " TRACE:"
        lines = open(self.path, 'r').readlines()
        traces = []
        linenum = 0
        for line in lines:
            linenum += 1
            if line.find(patn) > 0:
                traces.append((linenum, line))
        return traces

    def removeFile(self):
        if os.path.exists(self.path):
            os.remove(self.path)

if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         usage()
#         exit()
#     p = Parser(sys.argv[1])
#     p.dump()

    input = r"D:\Launcher_Profile\adblog_test.log"
    output = r"D:\Launcher_Profile\profiletest_1117.html"
    
    f = fileUtil(output)
    f.removeFile()
    
    f = fileUtil(input)
    p = Parser(f.fileFilter())
    p.dump(output)
    print('Parse done, output file -> %s' %output)

    pass
