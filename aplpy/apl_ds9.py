import string
import numpy as np
from apl_ds9_util import *

def ds9type(line):
	return line.replace("# ","")
	
class ds9Parser(object):
	ds9Dict = {'box':'',}
	"""
	This class parses DS9 region files. This is used
	for the main APLpy class.
	"""
	def __init__(self, fileName, wcs):
		try:
			f = open(fileName,'r')
			self.file = f.read().splitlines()
			f.close()
		except:
			print "This is not a proper ds9 region file. It's spam!"
			return
			
		self.shapes = []
		
		self.wcs = wcs
		self.coord_sys = self.file[3]
			
		for line in self.file[4:]:
			
			shape = {}
			
			p1 = line.find("(") 
			p2 = line.find(")") 
			
			line_prefix = line[:p1]
			line_coords = line[p1+1:p2]
			line_format = line[p2:].replace("# ","")
			line_format = line_format[2:]
			format = line_format.split(" ")
			
			shape['edgecolor'] = "g"
			shape['lw'] = None
			shape['ls'] = 'solid'
			
			
			for elem in format:
				arr = elem.split("=")
				if arr[0] == 'color':
					shape['edgecolor'] = arr[1]
				if arr[0] == 'width':
					shape['lw'] = arr[1]
				if arr[0] == 'dash':
					if arr[1] == "1": shape['ls'] = "dashed"
			shape['type'] = ds9type(line_prefix)
			shape['coord_sys'] = self.coord_sys
			coords = line_coords.split(",")
						
			if shape['type'] == 'circle':
				shape['x'] = float(coords[0])
				shape['y'] = float(coords[1])
				shape['radius'] = float(coords[2].replace('"',''))
			elif shape['type'] == 'box':
				shape['x'] = float(coords[0])
				shape['y'] = float(coords[1])
				shape['width'] = float(coords[2].replace('"',''))
				shape['height'] = float(coords[3].replace('"',''))
				shape['angle'] = float(coords[4])
			elif shape['type'] == 'line':
				shape['x'] = [float(coords[0]),float(coords[2])]
				shape['y'] = [float(coords[1]),float(coords[3])]
			elif shape['type'] == 'polygon':
				vertices = np.array(coords,float)
				n = vertices.size / 2
				vertices = vertices.reshape((2,n),order='F')
				shape['v'] = vertices.tolist()			
				
			self.shapes.append(shape)
					
	def plot(self):
		
		patches = []
		
		for shape in self.shapes:
												
			if shape['type'] == 'circle':
				shape = dict2pix(shape,self.wcs)
				patches.append(circle_patch(**shape))
			elif shape['type'] == 'box':
				shape = dict2pix(shape,self.wcs)
				patches.append(box_patch(**shape))
			elif shape['type'] == 'line':
				shape = dict2pix(shape,self.wcs)
				patches.append(line_patch(**shape))				
				
		return patches