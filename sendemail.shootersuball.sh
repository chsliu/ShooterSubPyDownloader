#!/bin/bash 

#=================================
DIR=$(readlink -e $0)
DP0=$(dirname "$DIR")
TODAY=$(date +"%Y-%m-%d")
MONTH=$(date +"%Y-%m")

T=$1
T="${t//\//-}"
LOG1=/tmp/$(basename $0)$T-$TODAY-summary.txt
LOG2=/tmp/$(basename $0)$T-$TODAY.txt
TXT1=/tmp/$(basename $0).txt

#=================================
$DP0/ShooterSubAll.py $1 $DP0/ignore.txt avi mp4 mkv >$LOG2

#=================================
echo List of newly download subtitles:	 >$LOG1
grep -F ".zh" $LOG2						>>$LOG1

#=================================
# cat $LOG2
# cat $LOG1

#=================================
cp $0 $TXT1

NUMOFLINES=$(wc -l < $LOG1)
if [ "$NUMOFLINES" -gt "1" ]; then
	echo $1 sending report...
	echo "$(basename $0) $1" | mailx -s "[FileBot] $(basename $0) $1" -a $LOG1 -a $LOG2 -a $TXT1 chsliu@gmail.com
else
	echo $1 has no report.
fi

rm $LOG1 $LOG2 $TXT1
