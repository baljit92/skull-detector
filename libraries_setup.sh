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
				echo "It's all good"
				exit
			} ;;
			*) 
			{
				echo "Unsupported OS, exiting"
				exit
			} ;;
	esac
