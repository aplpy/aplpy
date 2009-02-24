import numpy
from math import pi,sin,cos,asin,acos

ra_ngp=192.859508333333
dec_ngp=27.1283361111111
l_cp=122.932
l_0=l_cp-90.
ra_0=ra_ngp+90.
dec_0=90.-dec_ngp

deg2rad=pi/180.

def gal2fk5(l,b):
	
	sind=sin(b*deg2rad)*sin(dec_ngp*deg2rad)+cos(b*deg2rad)*cos(dec_ngp*deg2rad)*sin((l-l_0)*deg2rad)

	dec=asin(sind)

	cosa=cos((l-l_0)*deg2rad)*cos(b*deg2rad)/cos(dec)
	sina=(cos(b*deg2rad)*sin(dec_ngp*deg2rad)*sin((l-l_0)*deg2rad)-sin(b*deg2rad)*cos(dec_ngp*deg2rad))/cos(dec)

	dec=dec/deg2rad

	if sina > 0.:
		ra=acos(cosa)
	else:
		ra=-acos(cosa)

	ra=ra/deg2rad+ra_0

	while 1:

		if ra>=0. and ra<=360. and dec>=-90. and dec<=90.: break

		if ra<0.   : ra=ra+360.
		if ra>360. : ra=ra-360.
		if dec<-90.: dec=dec+90.
		if dec>+90.: dec=dec-90.

	return ra,dec
	
def fk52gal(ra,dec):

	sinb=sin(dec*deg2rad)*cos(dec_0*deg2rad)-cos(dec*deg2rad)*sin((ra-ra_0)*deg2rad)*sin(dec_0*deg2rad)

	b=asin(sinb)

	cosl=cos(dec*deg2rad)*cos((ra-ra_0)*deg2rad)/cos(b)
	sinl=(sin(dec*deg2rad)*sin(dec_0*deg2rad)+cos(dec*deg2rad)*sin((ra-ra_0)*deg2rad)*cos(dec_0*deg2rad))/cos(b)

	b=b/deg2rad

	if sinl > 0.:
		l=acos(cosl)
	else:
		l=-acos(cosl)

	l=l/deg2rad+l_0

	while 1:

		if l>=0. and l<=360. and b>=-90. and b<=90.: break

		if l<0.   : l=l+360.
		if l>360. : l=l-360.
		if b<-90.: b=b+90.
		if b>+90.: b=b-90.

	return l,b
