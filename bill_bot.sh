#!/bin/sh

bot_id=$GROUPME_BOT_ID

declare -a names=("colin" "hanna" "mark" "katie" "tuggle" "andrew" "evan" "ibby" "jacob" "jay" "alayah" "carter" "nic" "zach")

size=${#names[@]}
index=$(($RANDOM % $size))
name=${names[$index]}

message="hi $name"

curl -d "{\"text\" : \"$message\", \"bot_id\" : \"$bot_id\"}" https://api.groupme.com/v3/bots/post
