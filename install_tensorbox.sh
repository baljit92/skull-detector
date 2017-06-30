#!/bin/bash

echo "Cloning TensorBox"
git clone http://github.com/russell91/tensorbox
cd tensorbox

# Setting up tensorbox by downloading required files

echo "Downloading..."

mkdir -p data && cd data

osType=$(uname)
	case "$osType" in
			"Darwin")
			{
				curl -O http://russellsstewart.com/s/tensorbox/inception_v1.ckpt
				mkdir -p overfeat_rezoom && cd overfeat_rezoom
				curl -O http://russellsstewart.com/s/tensorbox/overfeat_rezoom/save.ckpt-150000v2
			} ;;    
			"Linux")
			{
				wget --continue http://russellsstewart.com/s/tensorbox/inception_v1.ckpt
				mkdir -p overfeat_rezoom && cd overfeat_rezoom
				wget --continue http://russellsstewart.com/s/tensorbox/overfeat_rezoom/save.ckpt-150000v2
			} ;;
			*) 
			{
				echo "Unsupported OS, exiting"
				exit
			} ;;
	esac
cd ..
pwd
echo "Compiling Tensorflow libraries"
cd ../utils && make && cd ..