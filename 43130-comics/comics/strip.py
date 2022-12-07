# darius <wwwDOTranveerkunalDOTnet> 2006
#this import statement allows access to the karamba functions
import karamba
import datetime
import os
import string

#add new comics here
tot = 0
image = 0
offset = 0
path = 0
when = 0
lock = 0
current_comic = 0
current_tb = 0
current_name = 0
nametext = 0
current_date = 0
datalock = 0
hide = 0
show = 1
magick = 0
darker = 0
thinner = 0
random = 0
standalone = 0
count = 0
init = 0
left = 0
right = 0
up = 0
down = 0 

def getComicStrip(widget):
	global image
	global offset
	global when
	global path
	global lock

	when = datetime.datetime.utcnow() + datetime.timedelta(days=offset, hours=-8)
	if not lock:
		command = [path+"bin/comics.sh", path, str(image), str(magick), str(offset), str(darker), str(thinner)]
		karamba.executeInteractive(widget, command)
		print "Fired"
		karamba.changeText(widget, current_date, "Fetching")
		karamba.changeText(widget, current_name, "<RSI Break>")
		lock = 1
	pass
		
def showComicStrip(widget):
	global image
	global width
	global current_comic
	global current_tb
	global current_name
	global current_date
	global path
	global when
	global offset
	global hide
	global when
	global show
	global nametext
	global standalone
	global left
	global right
	global up
	global down

	if current_comic:
		karamba.deleteImage(widget, current_comic)
	comicpath = "~/.comicskaramba/"
	current_comic = karamba.createImage(widget, 0, 22, os.path.expanduser(comicpath+"strip.png"))
	t = karamba.getImageSize(widget, current_comic)
	if t[0] > 1000:
		karamba.resizeImage(widget, current_comic, 1000, (t[1]*1000)/t[0])
		t = karamba.getImageSize(widget, current_comic)	
	if t[1] > 600:	
		karamba.resizeImage(widget, current_comic, (t[0]*700)/t[1], 700)
		t = karamba.getImageSize(widget, current_comic)
	if current_tb:
		karamba.deleteImage(widget, current_tb)
	current_tb = karamba.createImage(widget, 0, 0, os.path.expanduser(comicpath+"toolbar.png"))
	karamba.resizeImage(widget, current_tb, t[0]+10, 22)
	if hide:
		karamba.deleteImage(widget, hide)
	if left:
		karamba.deleteImage(widget, left)
	if right:
		karamba.deleteImage(widget, right)
	if up:
		karamba.deleteImage(widget, up)
	if down:
		karamba.deleteImage(widget, down)

	if standalone:
		left = karamba.createImage(widget, t[0] - 66, 0, "img/left.png")
		karamba.attachClickArea(widget, left)
		right = karamba.createImage(widget, t[0] - 44, 0, "img/right.png")
		karamba.attachClickArea(widget, right)
		up = karamba.createImage(widget, t[0] - 88, 0, "img/up.png")
		karamba.attachClickArea(widget, up)
		down = karamba.createImage(widget, t[0] - 22, 0, "img/down.png")
		karamba.attachClickArea(widget, down)
		hide = 0
	else:
		hide = karamba.createImage(widget, t[0] - 22, 0, "img/hide.png")
		karamba.attachClickArea(widget, hide)
		left = 0
		right = 0
		up = 0
		down = 0
	if current_name:
		karamba.deleteText(widget, current_name)
	current_name = karamba.createText(widget, 5, 3, t[0]/3, 22, nametext)
	karamba.changeTextColor(widget, current_name, 0, 0, 0)
	karamba.changeTextSize(widget, current_name, 17)
	karamba.changeTextFont(widget, current_name, "GEORGIA")
	if current_date:
		karamba.deleteText(widget, current_date)
	current_date = karamba.createText(widget, t[0]/3, 3, t[0]/3, 22, when.strftime("%d %B"))
	karamba.changeTextColor(widget, current_date, 0, 0, 0)
	karamba.changeTextSize(widget, current_date, 17)
	karamba.setTextAlign(widget, current_date, "CENTER")
	karamba.changeTextFont(widget, current_date, "GEORGIA")
	w = t[0]
	h = t[1] + 22
	if t[0] == 0 or not show:
		w = 0
		h = 0
	karamba.resizeWidget(widget, w, h)	
	pass

def initWidget(widget):	
	global path
	global tot	
	global lock
	global magick
	global darker
	global thinner
	global random
	global init
	global standalone
	
	path = karamba.getThemePath(widget)

	karamba.addMenuConfigOption(widget, "magick", "ImageMagick support")
	karamba.addMenuConfigOption(widget, "darker", "Darker Image")
	karamba.addMenuConfigOption(widget, "thinner", "Thinner Image")
	karamba.addMenuConfigOption(widget, "random", "Cycle Comics")
	karamba.addMenuConfigOption(widget, "standalone", "No Controller")
		
	magick = karamba.readMenuConfigOption(widget, "magick")
	darker = karamba.readMenuConfigOption(widget, "darker")
	thinner = karamba.readMenuConfigOption(widget, "thinner")
	random = karamba.readMenuConfigOption(widget, "random")	
	standalone = karamba.readMenuConfigOption(widget, "standalone")
	
	if not lock:
		command = [path+"bin/comics.sh", path, "initcheck", str(magick), str(darker), str(thinner)]
		karamba.executeInteractive(widget, command)
		print "InitCheck"
		lock = 1
	getComicStrip(widget)
	init = 1
	pass

def widgetUpdated(widget):
	global image
	global offset
	global datalock
	global tot
	global show
	global count
	global random
	global init
	
	refresh = 1

	if random:
		count = count + 1
		if count > 60:
			count = 0
			image = (image + 1) % tot
			getComicStrip(widget)
			
	data = karamba.getIncomingData(widget)
	if not datalock :
		if data == "s":
			show = 1
			refresh = 1
			datalock = 1		
		elif data == "c":
			refresh = 1
			datalock = 1		
		elif data == "d":
			offset = offset - 1
			datalock = 1	
			if offset < -29:
				refresh = 0
				offset = -29
		elif data == "u":
			offset = offset + 1
			datalock = 1	
			if offset > 0:
				refresh = 0
				offset = 0
		elif data == "r":
			image = (image + 1) % tot
			datalock = 1	
		elif data == "l":
			image = (image + tot -1) % tot
			datalock = 1	
		else:
			refresh = 0

		if refresh:
			getComicStrip(widget)
			
	if datalock and data == "b":
		datalock = 0
		
	if init:
		getComicStrip(widget)
		init = 0
		
	pass

def menuOptionChanged(widget, key, value):
	global magick
	global darker
	global thinner
	global random
	global standalone

	magick = karamba.readMenuConfigOption(widget, "magick")
	darker = karamba.readMenuConfigOption(widget, "darker")
	thinner = karamba.readMenuConfigOption(widget, "thinner")
	random = karamba.readMenuConfigOption(widget, "random")
	standalone = karamba.readMenuConfigOption(widget, "standalone")
	getComicStrip(widget)

	pass

def widgetClicked(widget, x, y, button):
	global image
	global tot
	global lock

	if not lock:
		if button == 4:
			image = (image + 1) % tot
			getComicStrip(widget)	
		elif button == 5:
			image = (image + tot -1) % tot
			getComicStrip(widget)
	pass

def meterClicked(widget, meter, button):
	global show
	global image
	global offset
	
	refresh = 1
	if button == 1:
		if meter == hide:
			karamba.resizeWidget(widget, 0, 0)
			show = 0
			refresh = 0
		elif meter == down:
			offset = offset - 1
			if offset < -29:
				refresh = 0
				offset = -29
		elif meter == up:
			offset = offset + 1
			if offset > 0:
				refresh = 0
				offset = 0
		elif meter == right:
			image = (image + 1) % tot
		elif meter == left:
			image = (image + tot -1) % tot
		if refresh:
			getComicStrip(widget)
			
	pass

def commandOutput(widget, pid, output):
	global lock
	global nametext
	global tot

	print "Returned: "+output
	if tot == 0:
		tot = string.atoi(output)
	else:
		nametext = output
	showComicStrip(widget)	
	lock = 0
	pass

# This will be printed when the widget loads.
print "Loaded Comics Extension : Strip"

