#!/bin/bash
IFS="\n"

LOG=$HOME"/fixtext.log"
#LOG="/dev/null"
echo "------------" >> "$LOG"

export YDOTOOL_SOCKET=/tmp/.ydotool.socket

BUFFER="$(xsel)"
printf "BUFFER = \"%s\"\n" $BUFFER >> "$LOG"

#if [ -z "$BUFFER" ] && [ $# -gt 0 ]; then
#    printf "111\n" >> "$LOG"
#    if [ "$1" == "-l" ] || [ "$1" == "--line" ]; then
#        printf "222\n" >> "$LOG"
##        ydotool key 19b:0
#        # shift+left
#        ydotool key 42:1
#        ydotool key 105:1
#        ydotool key 105:0
#        ydotool key 42:0
#        BUFFER="$(xsel)"
#        printf "BUFFER = \"%s\"\n" $BUFFER >> "$LOG"
##        exit 0
##        sleep 0.1
#    else
#        printf "333\n" >> "$LOG"
#        printf "Usage: fixtext [-l|--line]\n" >> /dev/stderr
#        exit 1
#    fi
#fi


if [ -z "$BUFFER" ]; then
    printf "Buffer is empty\n" >> "$LOG"
    exit 1
fi

BACKUP="$(xsel -b)"
printf "BACKUP = \"%s\"\n" $BACKUP >> "$LOG"

FIXED=$(echo "$BUFFER" | sed "y/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]{};':\",.\/<>?@#\$^&\`~фисвуапршолдьтщзйкыегмцчняФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯхъХЪжэЖЭбюБЮ№ёЁ/фисвуапршолдьтщзйкыегмцчняФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯхъХЪжэЖЭбю.БЮ,\"№;:?ёЁabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]{};':\",.<>#\`~/")
printf "FIXED = \"%s\"\n" $FIXED >> "$LOG"

printf "%s" "$FIXED" | xsel -bi

sleep 0.1

#ctrl+v
ydotool key 29:1
ydotool key 47:1
sleep 0.1
ydotool key 47:0
ydotool key 29:0

#sleep 0.1
#alt+shift
#ydotool key 56:1
#ydotool key 42:1
#ydotool key 42:0
#ydotool key 56:0

#sleep 0.1

printf "%s" "$BACKUP" | xsel -bi

xsel -c

