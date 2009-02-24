from scipy import *
import string as s
# deg2ra converts a single number into RA values. The output is an 3rd order array. 
# The array allows easy parsing for making RA axes text. EB
def deg2ra(x):
	h, r = divmod(x,15)
	m, s = divmod(r*240,60)
	if s >= 59.99:
		s = 0.
		m = m+1
	if m >= 60:
		m = 0
		h = h+1
	if h >= 23.99:
		h = 0
	h = "%02d" % h
	m = "%02d" % m
	s = str(round(s,2))
	s, decimal = s.split('.')
	s = "%02d" % float(s)
	decimal = "%02d" % float(decimal)
	s = s + '.' + decimal
	
	return array([h,m,s])

def deg2dec(x):
	if x >= 0:
		d, r = divmod(x,1)
		m, s = divmod(r*3600,60)
		if s >= 59.99:
			s = 0.
			m = m+1
		if m >= 60:
			m = 0
			d = d+1
		if d >= 90:
			d = 0
		d = " %02d" % d
		m = "%02d" % m
		s = str(round(s,2))
		s, decimal = s.split('.')
		s = "%02d" % float(s)
		decimal = "%02d" % float(decimal)
		s = s + '.' + decimal
	else:
		x = -1*x
		d, r = divmod(x,1)
		m, s = divmod(r*3600,60)
		if s >= 59.99:
			s = 0.
			m = m+1
		if m >= 60:
			m = 0
			d = d+1
			if d >= 90:
				d = 0
		d = "-%02d" % d
		#d = '-' + d
		m = "%02d" % m
		s = str(round(s,2))
		s, decimal = s.split('.')
		s = "%02d" % float(s)
		decimal = "%02d" % float(decimal)
		s = s + '.' + decimal
		
#		string = "-%02dd%02d'%02d.%02d" % (d,m,s,decimal)
		
	return array([d,m,s])

# This function will take an array that is produced from either deg2ra or deg2dec 
# and create a string with ":". EB
def arr2strRA(x, form='hh:mm:ss.ss'):

	txt = "$"+x[0]+"^h"

	if ":mm" in form: txt = txt + x[1] + "^m"
	if ":ss" in form:
		if ".ss" in form:
			txt = txt + x[2]
		else:
			txt = txt + x[2][0:2]
		txt = txt + "^s"
	txt = txt + "$"

	return txt

def arr2strDec(x, form='hh:mm:ss.ss'):
	txt = "$"+x[0]+"^{\circ}"

	if ":mm" in form: txt = txt + x[1] + "^{\prime}"
	if ":ss" in form:
		if ".ss" in form:
			txt = txt + x[2]
		else:
			txt = txt + x[2][0:2]
		txt = txt + "^{\prime\prime}"
	txt = txt + "$"

	return txt

# Changed from array to scalar - TR
# Precision is equated to default because it applies to both HMS and decimal. 
# Will put precision options for HMS over the weekend. EB
def raer(x, form = 'hh:mm:ss.ss'):
	if ':' in form:
		ra = deg2ra(x)
		st = arr2strRA(ra, form=form)
		return st
	elif 'dd.' in form:
		first, second = form.split('.')
		st = round(x,len(second))
		trail = '%5.'+str(len(second))+'f'
		return trail % st
	else:
		print "The wcsType chosen is not recognized. Defaulting to hh:mm:ss.ss.\n If you want coordinates given in degrees type form = 'dd.ddd' for example. "
		ra = deg2ra(x)
		st = arr2strRA(ra)
		return st
		
def decer(x, form = 'dd:mm:ss.ss'):
	if ':' in form:
		dec = deg2dec(x)
		st = arr2strDec(dec, form=form)
		return st
	elif 'dd.' in form:
		first, second = form.split('.')
		st = round(x,len(second))
		trail = '%5.'+str(len(second))+'f'
		return trail % st
	else:
		print "The wcsType chosen is not recognized. Defaulting to hh:mm:ss.ss.\n If you want coordinates given in degrees type form = 'dd.ddd' for example. "
		dec = deg2dec(x)
		st = arr2strDec(dec)
		return st

