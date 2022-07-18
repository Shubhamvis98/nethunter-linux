<h1>USB Arsenal for PinePhone</h1>

<img src="https://user-images.githubusercontent.com/43336210/178138927-de64a753-8b17-4345-b909-ae36412432a7.jpg" width="300px">


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
