#!/bin/bash

#Colour Output
RED="\033[01;31m"
BOLD="\033[01;01m"
RESET="\033[00m"

banner()
{
clear
cat <<'eof'
   _  __    __  __ __          __         
  / |/ /__ / /_/ // /_ _____  / /____ ____
 /    / -_) __/ _  / // / _ \/ __/ -_) __/
/_/|_/\__/\__/_//_/\_,_/_//_/\__/\__/_/   

eof
echo -e "\n${BOLD}Developer: Shubham Vishwakarma${RESET}"
echo -e "${BOLD}Git: ShubhamVis98${RESET}"
echo -e "${BOLD}Web: https://fossfrog.in${RESET}"
echo -e '____________________________________________________________________\n'
}

banner

[ `id -u` -ne 0 ] && echo -e "${RED}[!]Run as root${RESET}" && exit 1

install_dir='/usr/lib/nethunter'
desktop_file='/usr/share/applications/nethunter.desktop'
icon_path='/usr/share/icons/hicolor/scalable/apps/in.fossfrog.nethunter.svg'

case $1 in
	install)
		mkdir -v $install_dir
		cp -rv `basename $icon_path` $icon_path
		cp -rv nethunter.py nethunter.ui nhlauncher bin $install_dir
		cp -v nethunter.desktop $desktop_file
		chown root:root -R $install_dir
		chmod 644 $desktop_file
		chmod +x $install_dir/nethunter.py
		gtk-update-icon-cache /usr/share/icons/hicolor

		echo '[+]Installation Completed'
		;;
	uninstall)
		[ ! -d $install_dir ] && echo "Nethunter not found." && exit
		rm -v $icon_path
		rm -vrf $install_dir
		rm -v $desktop_file

		echo '[+]Removed'
		;;
	*)
		echo -e "${RED}Usage:${RESET}"
		echo -e "\t$0 install"
		echo -e "\t$0 uninstall"
esac