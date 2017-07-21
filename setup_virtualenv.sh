#!/bin/bash

# The below instrutctions are for Python 2.7

echo "Installing virtualenv"

# Execite commands based on OS type
osType=$(uname)
	case "$osType" in
			"Darwin")
			{
			   sudo pip install --upgrade virtualenv 
			} ;;    
			"Linux")
			{
			   sudo apt-get install python-pip python-dev python-virtualenv
			} ;;
			*) 
			{
				echo "Unsupported OS, exiting"
				exit
			} ;;
	esac

echo "Creating virtualenv in the current directory"
virtualenv --system-site-packages .

echo "Activate the viratualenv"
source ./bin/activate
