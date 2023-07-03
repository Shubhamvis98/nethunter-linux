#!/bin/bash

[ `id -u` -ne 0 ] && echo '[!]Run as root' && exit 1

nhdir='/usr/lib/nethunter'
rm -vrf $nhdir
rm -v /usr/share/applications/nethunter.desktop

echo '[+]Removed'
