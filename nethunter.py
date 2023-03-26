#!/usr/bin/python3
# Author Shubham Vishwakarma
# git/twitter: ShubhamVis98

import gi, subprocess, psutil, random
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gio, Notify
from bin import ducky


class Functions:
    def get_output(self, cmd, shell=False, wait=True):
        if shell:
            run = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        else:
            run = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = str(run.communicate()[0].decode()) if wait else ''
        returncode = run.poll()
        return [output, returncode, run]
    
    def notification(self, msg):
        try:
            msg = Notify.Notification.new(msg)
            msg.show()
        except:
            pass

    def start_monitor_mode(self, iface, mode=0):
        '''
        mode:
            0 ---> airmon-ng
            1 ---> iwconfig
        '''
        self.get_output(f'ip link set {iface} down')
        if mode == 0:
            self.get_output(f'airmon-ng start {iface}')
        elif mode ==1:
            self.get_output(f'iwconfig {iface} mode monitor')
        self.get_output(f'ip link set {iface} up')


    def stop_monitor_mode(self, iface, mode=0):
        '''
        mode:
            0 ---> airmon-ng
            1 ---> iwconfig
        '''
        self.get_output(f'ip link set {iface} down')
        if mode == 0:
            self.get_output(f'airmon-ng stop {iface}')
        elif mode ==1:
            self.get_output(f'iwconfig {iface} mode managed')
        self.get_output(f'ip link set {iface} up')


class Arsenal(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.usbarsenal = './bin/usbarsenal'
        self.function = self.builder.get_object('function')
        self.idVen = self.builder.get_object('idVen')
        self.idProd = self.builder.get_object('idProd')
        self.manufact = self.builder.get_object('manufact')
        self.prod = self.builder.get_object('prod')
        self.serialno = self.builder.get_object('serialno')
        self.btnEn = self.builder.get_object('enable')
        self.btnDis = self.builder.get_object('disable')
        self.status = self.builder.get_object('status')

        self.btnEn.connect('clicked', self.enable)
        self.btnDis.connect('clicked', self.disable)
        self.status_buffer = self.status.get_buffer()

    def run(self):
        self.setDefault()
    
    def getMassStoragePath(self):
        self.filechooser = self.builder.get_object('filechooser')
        return self.filechooser.get_filename()

    def setStatus(self, stsTxt):
        self.status_buffer.set_text(stsTxt)
    
    def getStatus(self):
        startIter, endIter = self.status_buffer.get_bounds()
        return(self.status_buffer.get_text(startIter, endIter, False))
    
    def setDefault(self):
        self.idVen.set_text('0x1D6B')
        self.idProd.set_text('0x0104')
        self.manufact.set_text('fossfrog')
        self.prod.set_text('HID Gadget')
        with open('/etc/machine-id', 'r')as macid:
            self.serialno.set_text(macid.read()[:-1])
        
        self.setStatus(self.get_output(f'{self.usbarsenal} -s')[0])

    def enable(self, btn):
        data = {
            'function': self.function.get_active_id(),
            'idvendor': self.idVen.get_text(),
            'idproduct': self.idProd.get_text(),
            'manufacturer': self.manufact.get_text(),
            'product': self.prod.get_text().replace(' ','_'),
            'serialno': self.serialno.get_text()
        }

        self.setStatus('')
        if data['function'] == 'null':
            self.setStatus('[?]Select Function First\n')
        elif '' in data.values():
            self.setStatus('[?]Fill Missing Details\n')
        else:
            if data['function'] == 'hid':
                self.setStatus(self.get_output(f'{self.usbarsenal} -h')[0])
            elif data['function'] == 'teth':
                self.setStatus(self.get_output(f'{self.usbarsenal} -t')[0])
            elif data['function'] == 'mass':
                self.setStatus(self.get_output(f'{self.usbarsenal} -m {self.getMassStoragePath()}')[0])
            data.pop('function')
            ARGS = ''
            for k, v in data.items():
                ARGS = f'{ARGS} --{k} "{v}"'
                self.setStatus(self.getStatus() + f'{k}: {"null" if v == "" else v}' + '\n')
            
            TMP = ARGS.split()
            ARGS = ''
            for i in range(len(TMP)):
                try:
                    TMP[i] = eval(TMP[i].replace('"',''))
                    ARGS = ARGS + ' ' + str(TMP[i])
                except:
                    ARGS = ARGS + ' ' + str(TMP[i])
            self.get_output(f'{self.usbarsenal} {ARGS}')[0]

    def disable(self, btn):
        self.setStatus(self.get_output(f'{self.usbarsenal} -d')[0])

class Ducky(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.editor = self.builder.get_object('ducky_editor')
        self.btnOpen = self.builder.get_object('open')
        self.btnClear = self.builder.get_object('clear')
        self.btnSave = self.builder.get_object('save')
        self.btnInject = self.builder.get_object('inject')

        self.btnOpen.connect('clicked', self.openInEditor)
        self.btnClear.connect('clicked', self.clearEditor)
        self.btnSave.connect('clicked', self.save)
        self.btnInject.connect('clicked', self.inject)

        self.editor_buffer = self.editor.get_buffer()

    def run(self):
        pass

    def clearEditor(self, btn):
        self.editor_buffer.set_text('')

    def inject(self, btn):
        startIter, endIter = self.editor_buffer.get_bounds()
        TMP = self.editor_buffer.get_text(startIter, endIter, False)
        ducky.inject_raw(TMP)
    
    def openInEditor(self, btn):
        filechooser = Gtk.FileChooserDialog(title="Open Ducky", parent=None, action=Gtk.FileChooserAction.OPEN)
        filechooser.add_buttons("_Open", Gtk.ResponseType.OK)
        filechooser.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)
        filechooser.set_default_response(Gtk.ResponseType.OK)
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            try:
                with open(filechooser.get_filename()) as f:
                    self.editor_buffer.set_text(f.read())
            except TypeError:
                buffer.set_text('Select File First...')
        filechooser.destroy()
    
    def save(self, btn):
        startIter, endIter = self.editor_buffer.get_bounds()
        TMP = self.editor_buffer.get_text(startIter, endIter, False)
        if TMP == '':
            self.notification('Editor is empty')
            return

        filechooser = Gtk.FileChooserDialog(title="Open Ducky", parent=None, action=Gtk.FileChooserAction.SAVE)
        filechooser.add_buttons("_Save", Gtk.ResponseType.OK)
        filechooser.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)
        filechooser.set_default_response(Gtk.ResponseType.OK)
        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            try:
                with open(filechooser.get_filename(), 'w') as f:
                    f.write(TMP)
                    self.notification('File Saved')
            except PermissionError:
                self.notification('File Not Saved, !!!Access Denied!!!')
        filechooser.destroy()

class MACChanger(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.maciface = self.builder.get_object('maciface')
        self.currentmac = self.builder.get_object('currentmac')
        self.newmac = self.builder.get_object('newmac')
        self.btnranmac = self.builder.get_object('btn_ranmac')
        self.btnchmac = self.builder.get_object('btn_chmac')
        self.btnrstmac = self.builder.get_object('btn_rstmac')

        self.maciface.connect('changed', self.on_iface_change)
        self.btnranmac.connect('clicked', self.gen_random_mac)
        self.btnchmac.connect('clicked', self.chmac)
        self.btnrstmac.connect('clicked', self.reset_mac)

    def run(self):
        ifaces = self.getifaces()
        for i in ifaces:
            self.maciface.append_text(i)
        self.maciface.set_active(0 if 'wlan0' not in ifaces else ifaces.index('wlan0'))

    def getifaces(self):
        tmp = psutil.net_if_addrs()
        iface_list = sorted(list(tmp.keys()))
        return iface_list
    
    def getmac(self, iface):
        tmp = psutil.net_if_addrs()
        for i in range(len(tmp[iface])):
            if 'AddressFamily.AF_PACKET' in str(tmp[iface][i]):
                return tmp[iface][i][1]

    def on_iface_change(self, iface):
        curmac = self.getmac(iface.get_active_text())
        self.currentmac.set_text(curmac)
    
    def gen_random_mac(self, btn):
        mac = ':'.join((f'0{(hex(i)[2:])}' if i<16 else hex(i)[2:]) for i in [random.randint(0, 255) for i in range(6)])
        self.newmac.set_text(mac)
    
    def chmac(self, btn):
        ifname = self.maciface.get_active_text()
        newmac = self.newmac.get_text()
        if len(newmac) == 17:
            self.get_output(f'ip link set {ifname} down')
            out = self.get_output(f'macchanger -m {newmac} {ifname}')
            self.get_output(f'ip link set {ifname} up')
            if out[1] == 0:
                self.notification('*MAC CHANGED: *')
            else:
                self.notification('!!! MAC NOT CHANGED !!!')
        self.on_iface_change(self.maciface)

    def reset_mac(self, btn):
        ifname = self.maciface.get_active_text()
        self.get_output(f'ip link set {ifname} down')
        out = self.get_output(f'macchanger -p {ifname}')
        self.get_output(f'ip link set {ifname} up')
        if out[1] == 0:
            self.notification('*MAC RESET DONE: *')
        else:
            self.notification('!!! MAC NOT CHANGED !!!')
        self.on_iface_change(self.maciface)

class Deauther(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.iface = self.builder.get_object('deauther_iface')
        self.btnscan = self.builder.get_object('btn_deauther_scan')
        self.display = self.builder.get_object('deauther_display')
        self.channel = self.builder.get_object('deauth_channel')
        self.btndeauth = self.builder.get_object('btn_deauth')

        self.btnscan.connect('clicked', self.deauther_scan)
        self.btndeauth.connect('clicked', self.deauther_start)
        self.display_buffer = self.display.get_buffer()

    def run(self):
        ifaces = MACChanger(self.builder).getifaces()
        for i in ifaces:
            self.iface.append_text(i)
        self.iface.set_active(0 if 'wlan0' not in ifaces else ifaces.index('wlan0'))


    def deauther_scan(self, btn):
        display = self.display_buffer
        ifname = self.iface.get_active_text()
        if ifname:
            out = self.get_output(f"iwlist {ifname} scanning | grep 'ESSID\|Frequency' | tac", shell=True)
            display.set_text(out[0].replace(' ', '').replace('Frequency', 'Freq').replace('Channel', 'Ch '))
        else:
            display.set_text('[!]Select Interface First')

    def deauther_start(self, btn):
        display = self.display_buffer
        channel = self.channel.get_text()
        ifname = self.iface.get_active_text()
        if ifname and channel:
            self.start_monitor_mode(ifname)
            self.run = self.get_output(f'mdk3 {ifname} d -c {channel}', wait=False)
        else:
            display.set_text('[!]Select Interface and Channel')

class NHGUI(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="in.fossfrog.nh")

    def do_activate(self):
        appname = 'NetHunter'
        builder = Gtk.Builder()
        builder.add_from_file("nethunter.ui")

        # Initialize Functions
        Arsenal(builder).run()
        Ducky(builder).run()
        MACChanger(builder).run()
        Deauther(builder).run()

        # Get The main window from the glade file
        window = builder.get_object("nh_main")
        window.set_title(appname)
        Notify.init(appname)

        # Show the window
        window.connect("destroy", Gtk.main_quit)
        window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


nh = NHGUI().run(None)
Gtk.main()
