# darius <wwwDOTranveerkunalDOTnet> 2006
#this import statement allows access to the karamba functions
import karamba

up = 0
left = 0
right = 0
down = 0
center = 0

lock = 0
path = 0

#this is called when you widget is initialized
def initWidget(widget):	
	global up
	global left
	global right
	global down
	global center
	global path

	path = karamba.getThemePath(widget)
	up = karamba.createImage(widget, 22, 0, "img/up.png")
	left = karamba.createImage(widget, 0, 22, "img/left.png")
	right = karamba.createImage(widget, 44, 22, "img/right.png")
	down = karamba.createImage(widget, 22, 44, "img/down.png")
	center = karamba.createImage(widget, 22, 22, "img/refresh.png")
	karamba.attachClickArea(widget, up)
	karamba.attachClickArea(widget, left)
	karamba.attachClickArea(widget, right)
	karamba.attachClickArea(widget, down)
	karamba.attachClickArea(widget, center)
	karamba.setIncomingData(widget, "strip", "c")
	print "Sleep"
	command = [path+"bin/comics.sh"]
	karamba.executeInteractive(widget, command)
	pass

def widgetUpdated(widget):
	karamba.setIncomingData(widget, "strip", "c")
	print "Sleep"
	command = [path+"bin/comics.sh"]
	karamba.executeInteractive(widget, command)
	pass

def meterClicked(widget, meter, button):
	global lock
	global path
	
	if not lock and button == 1:
		if meter == up:
			karamba.setIncomingData(widget, "strip", "u")
		elif meter == left:
			karamba.setIncomingData(widget, "strip", "l")
		elif meter == right:
			karamba.setIncomingData(widget, "strip", "r")
		elif meter == down:
			karamba.setIncomingData(widget, "strip", "d")
		elif meter == center:
			karamba.setIncomingData(widget, "strip", "s")
		lock = 1
		print "Sleep"
		command = [path+"bin/comics.sh"]
		karamba.executeInteractive(widget, command)
	
	pass

def commandOutput(widget, pid, output):
	global lock

	karamba.setIncomingData(widget, "strip", "b")
	print output
	lock = 0
	pass

# This will be printed when the widget loads.
print "Loaded Comics Extension"

