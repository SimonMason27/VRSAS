#!/bin/sh
rclone --config=/home/pi/.config/rclone/rclone.conf copy -v /home/pi/Documents/Data_from_Pi onedrive:Data_from_Pi
