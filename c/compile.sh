#/bin/bash
warn=`gcc -Wall -c socket.c -o main`
if [ -z $warn]; then
 copile=`gcc -o main socket.c`
else
 echo $warn
fi
