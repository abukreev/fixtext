#!/bin/bash

# (c) https://habr.com/ru/post/279499/

IFS="\n"

LOG="/home/abukreev/fixtext.log"
printf "\n" >> $LOG

BUFFER="$(xsel)"
printf "BUFFER = \"%s\"\n" $BUFFER >> $LOG

if [ "$BUFFER" = "" ]; then
    printf "Buffer is empty" >> $LOG
    exit 1
fi

BACKUP="$(xsel -b)"

FIXED=$(echo "$BUFFER" | sed "y/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]{};':\",.\/<>?@#\$^&\`~фисвуапршолдьтщзйкыегмцчняФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯхъХЪжэЖЭбюБЮ№ёЁ/фисвуапршолдьтщзйкыегмцчняФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯхъХЪжэЖЭбю.БЮ,\"№;:?ёЁabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]{};':\",.<>#\`~/")
printf "FIXED = \"%s\"\n" $FIXED >> $LOG

printf "%s" "$FIXED" | xsel -b -i

sleep 0.05

xdotool key ctrl+v
xdotool key alt+shift

printf "%s" "$BACKUP" | xsel -b -i

