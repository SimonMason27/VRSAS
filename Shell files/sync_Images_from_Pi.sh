#!/bin/sh

rclone --config=/home/pi/.config/rclone/rclone.conf copy -v /home/pi/Documents/Images_from_Pi onedrive:Images_from_Pi
