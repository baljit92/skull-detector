#!/usr/bin/env bash

pip install Pillow
osType=$(uname)
	case "$osType" in
			"Darwin")
			{
				brew install opencv
				brew install pkg-config
			} ;;    
			"Linux")
			{
			   sudo apt-get install python-pip python-dev python-virtualenv
			} ;;
			*) 
			{
				echo "Not supported"				
			} ;;
	esac
