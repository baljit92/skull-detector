#!/usr/bin/env bash

pip install Pillow
osType=$(uname)
	case "$osType" in
			"Darwin")
			{
				brew install pkg-config
			} ;;    
			"Linux")
			{
				sudo apt-get install pkg-config
				echo "It's all good"
				exit
			} ;;
			*) 
			{
				echo "Unsupported OS, exiting"
				exit
			} ;;
	esac
