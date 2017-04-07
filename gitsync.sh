#!/bin/bash 

#=================================
if [ "root" = $(whoami) ]; then
	echo "no sync while been root"
	exit
fi

#=================================
DIR=$(readlink -e "$0")
DP0=$(dirname "$DIR")

#=================================
$DP0/gitconf.sh

#=================================
if [ -z "$1" ]; then
	# echo Working in $DP0
	pushd "$DP0"
else
	# echo Working in $1
	pushd "$1"
fi

#=================================
git pull

git add .
git commit -a -m "Automated commit at $(date +"%D") $(date +"%T") on $(hostname)" 
git push
