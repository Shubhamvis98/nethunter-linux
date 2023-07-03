#!/bin/bash

[ `id -u` -ne 0 ] && echo '[!]Run as root' && exit 1

nhdir='/usr/lib/nethunter'
mkdir -v $nhdir
cp -rv bin logo.svg nethunter.py nethunter.ui nhlauncher $nhdir
cp -v nethunter.desktop /usr/share/applications/
chown root:root -R $nhdir
chmod 644 /usr/share/applications/nethunter.desktop

echo '[+]Installation Completed'