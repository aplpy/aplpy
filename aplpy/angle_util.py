import math

class Angle(object):
    
    def __init__(self,degrees=None,sexagesimal=None):

        if degrees:
            
            m,d = math.modf(degrees)
            s,m = math.modf(m*60.)
        
            d,m,s = int(round(d)),int(round(m)),s

            self.angle = (d,m,s)

        if sexagesimal:
            
            self.angle = sexagesimal
            
        self._simplify()
        
    def tostring(self,format='ddd:mm:ss',separators=[":",":",""]):
        
        l = self.tostringlist(format=format)
        
        string = ""
        if len(l) == 1:
            pass
        
        
    def tostringlist(self,format='ddd:mm:ss'):

        hours = 'h' in format
        format = format.replace('h','d')

        r = 1
        if 'mm' in format: r = 2
        if 'ss' in format: r = 3
        if '.s' in format:
             r = 4
             pos = format.find('.')
             n = len(format[pos+1:])
             r = r + n/10.
             
        tup = self._round(r)
            
        string = []
        
        if 'dd' in format:
            if type(tup) == tuple:
                string.append("%i" % tup[0])
            else:
                string.append("%i" % tup)
        if 'mm' in format:
            string.append("%02i" % tup[1])
        if 'ss' in format and not '.s' in format:
            string.append("%02i" % tup[2])
        if 'ss.s' in format:
            string.append(("%0"+str(n+3)+"."+str(n)+"f") % tup[2])
            
        return format + " = " + str(string)
#        str(self.angle)
        
    def _round(self,value):
        
        d = self.angle[0]
        m = self.angle[1]
        s = self.angle[2]
                
        if value < 2:
            d = round(d + m / 60. + s / 3600.)
            return (int(d))
        elif value < 3:
            m = round(m + s / 60.)
            return (d,int(m))    
        elif value < 4:
            s = round(s)
            return (d,m,int(s))
        else:
            n = int(round( ( value - 4. ) * 10 ))
            return (d,m,round(s,n))
            
#        d = "%i" % self.angle[0]
#        m = "%2i" % self.angle[1]
#        s = "%2i" % self.angle[2]
#        
#        if value==1:
#            return (d)
#        elif value==2:
#            return (d,m)
#        elif value==3:
#            return (d,m,s)
#        elif value >= 4:
#            n = int(round((value-4)*10))
#            print str(n)+"decimal places"
#            return (str(self.angle[0]),str(self.angle[1]),str(self.angle[2]),str(round(self.angle[3],n)))
                
    def __add__(self,other):

        s  = self.angle[2] + other.angle[2]
        m  = self.angle[1] + other.angle[1]
        d  = self.angle[0] + other.angle[0]

        s = Angle(sexagesimal=(d,m,s))
        s._simplify()

        return s
        
    def _simplify(self):
        
        d,m,s = self.angle
        
        while s >= 60.:
            m = m + 1
            s = s - 60.
        while m > 59:
            d = d + 1
            m = m - 60
        while d > 359:
            d = d - 360
                    
        self.angle = (d,m,s)
        
a = Angle(degrees=1.12512)
b = Angle(degrees=152312.4124)



print a.tostring(format='hh')
print a.tostring(format='dd')
print a.tostring(format='hh:mm')
print a.tostring(format='dd:mm')
print a.tostring(format='hh:mm:ss')
print a.tostring(format='dd:mm:ss')
print a.tostring(format='hh:mm:ss.s')
print a.tostring(format='hh:mm:ss.sssss')
