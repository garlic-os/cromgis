#!/bin/bash

# Configuration #
# To remove comics, just remove it from the list below, but to add any new comics, 
# you have to write the fetch code below and add it to the list.
# Similiarly you can adjust the low and high brightness and transparency
# darius <wwwDOTranveerkunalDOTnet> 2006
##############################################################################################################
comiclist=("calvin-hobbes" "dilbert" "garfield" "between-friends" "peanuts" "bornloser" "archie" "user-friendly" "foxtrot")
low_brightness=70
high_brightness=100
low_transparency=0.7 # alpha
high_transparency=0.5 # alpha
##############################################################################################################

brightness=0
transparency=0

if [ $# -eq 0 ]
	then
	sleep 1
	echo Awake
	exit 0
fi

if [ $2 == "initcheck" ]
	then
	if ! [ -e ~/.comicskaramba ]
		then
		mkdir ~/.comicskaramba
	fi
	cd ~/.comicskaramba
	for i in "${comiclist[@]}"
	  do
	  if ! [ -e $i ]
		  then
		  mkdir $i
	  fi
	done
	if [ -e strip.png ]
		then
		rm strip.png
	fi
	if [ -e toolbar.png ]
		then
		rm toolbar.png
	fi
	echo "${#comiclist[*]}"
	exit 0
fi

# If magick
magick=$3

# Get into the comics folder
cd ~/.comicskaramba

# Fetch Status
status=0

# Don't change this string, py file uses this logic
date=`date +%Y%m%d -d "$4 day -8 hour" -u`
image=$2
localfile=${comiclist[$image]}/${comiclist[$image]}$date.gif

if ! [ -e $localfile ]
	then
	case ${comiclist[$image]} in

# Configuration #
##############################################################################################################
        # Dilbert
		dilbert)
			curl -s http://www.dilbert.com/comics/dilbert/archive/dilbert-$date.html -o .html
			curl -s http://www.dilbert.com`cat .html | grep -e "/comics/dilbert/archive/images/dilbert[0-9]*\.gif" -e "/comics/dilbert/archive/images/dilbert[0-9]*\.jpg" -o -m 1` -o $localfile
			;;
		# Peanuts
		peanuts)
			curl -s http://www.snoopy.com/comics/peanuts/archive/peanuts-$date.html -o .html
			curl -s http://www.snoopy.com`cat .html | grep -e "/comics/peanuts/archive/images/peanuts[0-9]*\.gif" -e "/comics/peanuts/archive/images/peanuts[0-9]*\.jpg" -o -m 1` -o $localfile
			;;
        # Bornloser
		bornloser)
			curl -s http://www.comics.com/comics/bornloser/archive/bornloser-$date.html -o .html
			curl -s http://www.comics.com`cat .html | grep -e "/comics/bornloser/archive/images/bornloser[0-9]*\.gif" -e "/comics/bornloser/archive/images/bornloser[0-9]*\.jpg" -o -m 1` -o $localfile
			;;
        # Calvin & Hobbes
		calvin-hobbes)
			year=`date +%Y -d "$4 day -8 hour" -u`
			fetch_date=`date +%y%m%d -d "$4 day -8 hour" -u`
			curl -s http://images.ucomics.com/comics/ch/$year/ch$fetch_date.gif -e http://www.gocomics.com -o $localfile
			;;
		# Garfield
		garfield)
			year=`date +%Y -u`
			fetch_date=`date +%y%m%d -d "$4day -8 hour" -u`
			curl -s http://images.ucomics.com/comics/ga/$year/ga$fetch_date.gif -e http://www.gocomics.com -o $localfile
			;;
		# User Friendly
		user-friendly)
			fetch_date=`date +%Y%m%d -d "$4day -8 hour" -u`
			curl -s http://ars.userfriendly.org/cartoons/?id=$fetch_date -o .html
			curl -s `cat .html | grep -e "http://www.userfriendly.org/cartoons/archives/.*\.gif" -o -m 1` -o $localfile
			;;
		# Archie
		archie)
			fetch_date=`date +%d -d "$4day -8 hour" -u`
			curl -s http://www.archiecomics.com/pops_shop/dailycomics/image$fetch_date.gif -o $localfile
			;;
		# Foxtrot
		foxtrot)
			year=`date +%Y -u`
			fetch_date=`date +%y%m%d -d "$4day -8 hour" -u`
			curl -s http://images.ucomics.com/comics/ft/$year/ft$fetch_date.gif -e http://www.gocomics.com -o $localfile
			;;
		between-friends)
			fetch_date=`date +%Y%m%d -d "$4day -15 day -8 hour" -u`
			curl -s http://est.rbma.com/content/Between_Friends?date=$fetch_date -e http://www.betweenfriendscartoons.com/index.php -o $localfile
			;;
##############################################################################################################
		*)
			echo "No Strip Found"
			;;
	esac
	if [ $? -eq 0 ]
		then
		status=1
	else
		rm $localfile
	fi		
else
	status=2
fi

if [ $5 == 1 ]
	then
	brightness=$low_brightness
else
	brightness=$high_brightness
fi

if [ $6 == 1 ]
	then
	transparency=$high_transparency
else
	transparency=$low_transparency
fi

if ! [ status == 0 ]
	then
	if [ $magick == 1 ]
		then
		convert  $localfile -modulate $brightness -channel A -fx $transparency strip.png
		convert  $1/img/toolbar.png -modulate $brightness -channel A -fx $transparency toolbar.png
	else
		cp $localfile strip.png
		cp  $1/img/toolbar.png toolbar.png
	fi
fi

case $status in
	0)
		echo Failure
		;;
	1)
		echo ${comiclist[$image]}
		;;
	2)
		echo ${comiclist[$image]}
		;;
esac