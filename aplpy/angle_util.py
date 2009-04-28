import math
import numpy as np
import math_util

class Angle(object):
    
    def __init__(self,degrees='none',sexagesimal='none',latitude=False):
        
        if degrees <> 'none':
            
            # Find out if the angle is negative
            negative = degrees < 0
            
            # Treat angle as positive
            degrees = np.abs(degrees)
            
            # Decompose angle into degrees, minutes, seconds
            m,d = math.modf(degrees)
            s,m = math.modf(m*60.)
            s = s * 60.
            
            # Express degrees and minutes as integers
            d,m = int(round(d)),int(round(m))
            
            # Put back minus sign if negative
            if negative:
                d,m,s = -d,-m,-s
            
            # Set angle to tuple of degrees/minutes/seconds
            self.angle = (d,m,s)
        
        elif sexagesimal <> 'none':
            self.angle = sexagesimal
        
        # Whether to keep the angle between 0 and 360 or -90 and 90
        self.latitude = latitude
        
        self.negative = False
        
        self._simplify()
    
    def _simplify(self):
        
        # Decompose angle
        d,m,s = self.angle
        
        # Make sure seconds are between 0. (inclusive) and 60. (exclusive)
        r = np.mod(s,60.)
        m = m + int(round(s - r)) / 60
        s = r
        
        # Make sure minutes are between 0 and 59 (both inclusive)
        r = np.mod(m,60)
        d = d + (m - r) / 60
        m = r
        
        # Make sure degrees are between 0 and 359 (both inclusive)
        d = np.mod(d,360)
        
        # If angle is latitude, then:
        # - if degrees are between 90 and 270, angle is invalid
        # - if angle is between 270 and 360, subtract 360 degrees
        
        if self.latitude and d > 90:
            if d >= 270:
                self.negative = True
                d,m,s = 359 - d ,59 - m, 60. - s
                if s == 60.:
                    s = s - 60.
                    m = m + 1
                if m == 60:
                    m = m - 60.
                    d = d + 1
            else:
                raise Exception("latitude should be between -90 and 90 degrees")
        
        # Set new angle
        self.angle = (d,m,s)
    
    def todegrees(self):
        d,m,s = self.angle
        degrees = d + m/60. + s/3600.
        if self.negative:
            degrees = - degrees
        return degrees
    
    def tohours(self):
        
        d,m,s = self.angle
        
        rd = np.mod(d,15)
        h = (d - rd) / 15
        
        rm = np.mod(m,15)
        m = (m - rm) / 15 + rd * 4
        
        s = s / 15. + rm * 4.
        
        a = Angle(sexagesimal=(h,m,s),latitude=self.latitude)
        a.negative = self.negative
        
        return a
    
    def toround(self,rval=3):
        
        # Decompose angle
        d,m,s = self.angle
        
        # Round numbers:
        # 1: degrees only
        # 2: degrees and minutes
        # 3: degrees, minutes, and seconds
        # 4.n: degrees, minutes, and decimal seconds with n decimal places
        
        if rval < 2:
            n = int(round( ( rval - 1. ) * 100 ))
            d = round(d + m / 60. + s / 3600.,n)
            if n==0:
                d = int(d)
            return d
        elif rval < 3:
            m = int(round(m + s / 60.))
            if m == 60:
                m = 0
                d = d + 1
            return (d,m)
        elif rval < 4:
            s = int(round(s))
            if s == 60:
                s = 0
                m = m + 1
            if m == 60:
                m = 0
                d = d + 1
            return (d,m,s)
        else:
            n = int(round( ( rval - 4. ) * 100 ))
            s = round(s,n)
            if s == 60.:
                s = 0.
                m = m + 1
            if m == 60:
                m = 0
                d = d + 1
            return (d,m,s)
    
    def tostringlist(self,format='ddd:mm:ss',sep=("d","m","s")):
        
        format = format.replace('h','d')
        
        r = 1
        if '.d' in format:
             r = 1
             pos = format.find('.')
             nd = len(format[pos+1:])
             r = r + nd/100.
        if 'mm' in format: r = 2
        if 'ss' in format: r = 3
        if '.s' in format:
             r = 4
             pos = format.find('.')
             ns = len(format[pos+1:])
             r = r + ns/100.
        
        tup = self.toround(rval=r)
        if type(tup) == tuple:
            tup = list(tup)
        else:
            tup = [tup]
        
        string = []
        
        if 'dd' in format:
            if '.d' in format:
                string.append(("%0"+str(nd+3)+"."+str(nd)+"f") % tup[0]  + sep[0])
            else:
                string.append("%i" % tup[0] + sep[0])
        if 'mm' in format:
            string.append("%02i" % tup[1] + sep[1])
        if 'ss' in format and not '.s' in format:
            string.append("%02i" % tup[2] + sep[2])
        if 'ss.s' in format:
            string.append(("%0"+str(ns+3)+"."+str(ns)+"f") % tup[2]  + sep[2])
        
        if self.latitude:
            if self.negative:
                string[0] = "-" + string[0]
            else:
                string[0] = "+" + string[0]
        
        return string
    
    def __add__(self,other):
        
        s  = self.angle[2] + other.angle[2]
        m  = self.angle[1] + other.angle[1]
        d  = self.angle[0] + other.angle[0]
        
        s = Angle(sexagesimal=(d,m,s),latitude=self.latitude)
        s._simplify()
        
        return s
    
    def __mul__(self,other):
        
        d,m,s = self.angle
        s = s * other
        m = m * other
        d = d * other
        
        if self.latitude and self.negative:
            d,m,s = -d,-m,-s
        
        s = Angle(sexagesimal=(d,m,s),latitude=self.latitude)
        s._simplify()
        
        return s

def smart_round_angle(x,latitude=False):
    
    d,m,s = 0,0,0.
    
    divisors_360 = math_util.divisors(360)
    divisors_10 = math_util.divisors(10)
    divisors_60 = math_util.divisors(60)
    
    if x >= 1:
        d = math_util.closest(divisors_360,x)
    else:
        x = x * 60.
        if x >= 1:
            m = math_util.closest(divisors_60,x)
        else:
            x = x * 60.
            if x >= 1:
                s = math_util.closest(divisors_60,x)
            else:
                t = 1.
                while True:
                    t = t * 10.
                    x = x * 10.
                    if x >= 1:
                        s = math_util.closest(divisors_10,x) / t
                        break
    
    a = Angle(sexagesimal=(d,m,s),latitude=latitude)
    
    return a
