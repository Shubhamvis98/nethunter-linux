<h2>NETHUNTER for PinePhone</h2>

<h3>GUI: <code>python nethunter.py</code></h3>
<h2>Preview:</h2>
<img width="400px" src="https://user-images.githubusercontent.com/43336210/226916474-395781f5-2fb0-459e-84f6-693245a746dd.gif">
<h2>Features:</h2>
<ul>
    <li>Keyboard and Mouse Input Working</li>
    <li>USB Mass Storage Working</li>
    <li>USB Tethering</li>
    <li>Ducky [A minimal Rucky like implementation]</li>
    <li>MAC Changer GUI Added</li>
</ul>
<h3>You can use all the above features through command-line as well if you don't want to use GUI</h3>
<h3>Command: <code>bin/usbarsenal</code></h3>
<pre>
 _ _  ___  ___   ___  ___  ___  ___  _ _  ___  _
| | |/ __>| . > | . || . \/ __>| __>| \ || . || |
| ' |\__ \| . \ |   ||   /\__ \| _> |   ||   || |_
`___'<___/|___/ |_|_||_\_\<___/|___>|_\_||_|_||___|
______________________________________for_PinePhone
github|twitter: ShubhamVis98

USAGE:
        usbarsenal [OPTION] [FILE]
        -u #Usage
        -s #Status
        -h #Enable HID e.g. Keyboard and Mouse
        -t #Enable USB Tethering
        -m [Block/File Path to mount] #Enable Mass Storage
        -d Disable All
Optional Args:
        --idvendor [Vendor ID]
        --idproduct [Product ID]
        --manufacturer [Manufacturer]
        --product [Product]
        --serialno [Serial No.]
</pre>
<h3>Command: <code>python bin/ducky.py</code></h3>
<pre>
  ___  _   _  ___ _  ____   __  ___ _  _    _ ___ ___ _____ ___  ___ 
 |   \| | | |/ __| |/ /\ \ / / |_ _| \| |_ | | __/ __|_   _/ _ \| _ \
 | |) | |_| | (__| ' <  \ V /   | || .` | || | _| (__  | || (_) |   /
 |___/ \___/ \___|_|\_\  |_|   |___|_|\_|\__/|___\___| |_| \___/|_|_\
__________________________________________________________by fossfrog

USAGE: ducky.py [OPTION] [FILE/TEXT]
        -h      Help
        -f      Ducky_Script
        -t      Text
</pre>

<h2>Source:</h2>
<ul>
    <li>https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt</li>
    <li>http://www.linux-usb.org</li>
</ul>
