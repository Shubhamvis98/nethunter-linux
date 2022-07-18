<pre>
 _ _  ___  ___   ___  ___  ___  ___  _ _  ___  _
| | |/ __>| . > | . || . \/ __>| __>| \ || . || |
| ' |\__ \| . \ |   ||   /\__ \| _> |   ||   || |_
`___'<___/|___/ |_|_||_\_\<___/|___>|_\_||_|_||___|
______________________________________for_PinePhone
github|twitter: ShubhamVis98
1) Enable Keyboard/Mouse
2) Enable and Set Mass Storage Image
3) Enable Tethering
4) Disable All with Core
5) Exit

Select Option:
</pre>
<h2>Installation:</h2>
<ul>
    <h3>Using Makefile</h3>
    <ul>
        <li>Execute: <code>make && make install</code></li>
    </ul>
</ul>
<ul>
    <h3>Manual Installation</h3>
    <ol>
        <li>Compile hid-gadget-test, rename the executable as "hidg" and put in "/usr/local/bin"</li>
        <li>Copy/Move usbarsenal, duckyconverter and duckyprint in "/usr/local/bin"</li>
    </ol>
</ul>

<h2>Features:</h2>
<ul>
    <li>Keyboard and Mouse Input Working</li>
    <li>USB Mass Storage Working</li>
    <li>USB Tethering</li>
</ul>

<h2>Source:</h2>
<ul>
    <li>Nethunter duckyconverter script <b>[Works fine after some modifications]</b></li>
    <li>https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt</li>
    <li>http://www.linux-usb.org</li>
    <li>https://github.com/pelya/android-keyboard-gadget</li>
</ul>
