#!/bin/bash
IFS="\n"

#LOG=$HOME"/fixtext.log"
LOG="/dev/null"
echo "------------" >> "$LOG"

BUFFER="$(xsel)"
printf "BUFFER = \"%s\"\n" $BUFFER >> "$LOG"

if [ -z "$BUFFER" ] && [ $# -gt 0 ]; then
    printf "111\n" >> "$LOG"
    if [ "$1" == "-l" ] || [ "$1" == "--line" ]; then
        printf "222\n" >> "$LOG"
#        xdotool keyup Ctrl
        xdotool keyup Pause
        xdotool key Shift+Left
        BUFFER="$(xsel)"
        printf "BUFFER = \"%s\"\n" $BUFFER >> "$LOG"
#        exit 0
#        sleep 0.1
    else
        printf "333\n" >> "$LOG"
        printf "Usage: fixtext [-l|--line]\n" >> /dev/stderr
        exit 1
    fi
fi


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

xdotool key ctrl+v

#sleep 0.1

xdotool key alt+shift

#sleep 0.1

printf "%s" "$BACKUP" | xsel -bi

xsel -c

