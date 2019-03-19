#!/bin/bash

echo "Installing project files to ~/.pihole-display"
## Create the project directory in the users' home folder
mkdir ~/.pihole-display
## Copy the fonts folder over
cp -r fonts ~/.pihole-display/fonts
## Copy the display script over
cp display-stats.py ~/.pihole-display/display-stats.py

## Add to the users .bashrc file to autostart the display script
echo "Adding startup line to ~/.bashrc"
echo "
sudo python ~/.pihole-display/display-stats.py &
" >> ~/.bashrc

## Alert the user that they should either log out and back in again
## or source their bashrc file
echo "You should log out and back in again or source your bashrc file now."
