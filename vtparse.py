import os
import sys
import re
import png

def tobin(x, count=8):
        """
        Integer to binary
        Count is number of bits
        """
        return "".join(map(lambda y:str((x>>y)&1), range(count-1, -1, -1)))

def chartosixel(c):
    return ord(c) - 077

#  7x10 char matrix
class vtchar:
    m = []
    charcode = 0

    def __init__(self, code):
        self.m = [' ' for x in range(7*10)]
        self.charcode = code

    def sixel(self, nsixel, topbottom, c):
        bits = chartosixel(c)
        rang3 = range(6 - 2*topbottom)
        for b in rang3:
            bit = (bits>>b) & 001
            self.m[(topbottom*6+b)*7 + nsixel] = '01'[bit]

    def sixelpack(self, spair):
        sp = spair.strip().split('/')
        for tb in [0,1]:
            for sc in range(7):
                self.sixel(sc,tb,sp[tb][sc])

    def dump(self):
        i = 0
        for c in self.m:
            print c,
            i = i + 1
            if i % 7 == 0: print('\n')

    def writepng(self):
        # pack
        s=[]
        i = 0
        b = 0
        for c in self.m:
            i = i + 1
            b = b | (int(c)<<(9-((i-1)%7)))
            if i % 7 == 0: 
                b = b | (b>>1)
                s.append(tobin(~b,10))
                s.append(tobin(~0,10))
                b = 0
        s = map(lambda x: map(int, x), s)
        
        f = open('u%04x.png'%self.charcode, 'wb')
        w = png.Writer(len(s[0]), len(s), greyscale=True, bitdepth=1)
        w.write(f, s)
        f.close()



print 'Opening file "VT200"...'
try:
    text = open('VT200').read().replace('\n', ' ')
except:
    print "error"
    sys.exit(1)

fontdef = re.compile('.*\033P([0-9]\;){5}[0-9]\{\s*[A-Za-z]+\s+(?P<sixels>[^\033]*)\033\/')
try:
    sixels = fontdef.match(text).expand('\g<sixels>')
except:
    print "VT200 doesn't seem to contain character definitions"
    sys.exit(2)

test=False
if test:
    v = vtchar(0)
    #v.sixelpack('~~~~~~~/~~~~~~~')
    #v.dump()
    v.sixelpack('ogcacgo/B?????B')
    v.dump()
    v.writepng()
    sys.exit(0)

charcode = 1024
for chardef in sixels.split(';'):
    v=vtchar(charcode)
    v.sixelpack(chardef)
    #v.dump()
    v.writepng()
    charcode = charcode + 1

