#!/bin/bash

query_ret=$(setxkbmap -query | grep layout)
layout=${query_ret#*:}

if test $layout = "us"
then
	$(setxkbmap de)
else
	$(setxkbmap us)
fi
	$(notify-send "Current Layout: $layout") 

