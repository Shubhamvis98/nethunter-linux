#!/usr/bin/python3
# Author Shubham Vishwakarma
# git/twitter: ShubhamVis98

import gi, subprocess, psutil, random, json, datetime
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gio, Pango, Notify
from bin import ducky
import os

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
    
    def prompt(self):
        dialog = Gtk.Dialog(title="Add Command")
        dialog.add_buttons(
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL
        )
        label = Gtk.Entry(text='Label', margin=5)
        cmd = Gtk.Entry(text='echo hello world', margin=5)
        dialog.vbox.pack_start(label, True, True, 0)
        dialog.vbox.pack_start(cmd, True, True, 0)
        dialog.show_all()

        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            label = label.get_text()
            cmd = cmd.get_text()
        elif response == Gtk.ResponseType.CANCEL:
            return None

        if (label and cmd) != '':
            return [label, cmd]
        else:
            return 1

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
        self.monmode = self.builder.get_object('deauth_mon_mode')
        self.btndeauth = self.builder.get_object('btn_deauth')

        self.btnscan.connect('clicked', self.deauther_scan)
        self.btndeauth.connect('clicked', self.deauther_run)
        self.display_buffer = self.display.get_buffer()

    def run(self):
        ifaces = MACChanger(self.builder).getifaces()
        for i in ifaces:
            self.iface.append_text(i)
        self.iface.set_active(0 if 'wlan0' not in ifaces else ifaces.index('wlan0'))
        mon_modes = ['airmon-ng', 'iwconfig']
        for i in mon_modes:
            self.monmode.append_text(i)
        self.monmode.set_active(1)


    def deauther_scan(self, btn):
        display = self.display_buffer
        ifname = self.iface.get_active_text()
        if ifname:
            out = self.get_output(f"iwlist {ifname} scanning | grep 'ESSID\|Frequency' | tac", shell=True)
            display.set_text(out[0].replace(' ', '').replace('Frequency', 'Freq').replace('Channel', 'Ch '))
        else:
            display.set_text('[!]Select Interface First')

    def deauther_run(self, btn):
        display = self.display_buffer
        channel = self.channel.get_text()
        ifname = self.iface.get_active_text()
        monmode = self.monmode.get_active()
        if self.btndeauth.get_label() == 'Start Deauther':
            if ifname and channel:
                self.start_monitor_mode(ifname, monmode)
                self.run = self.get_output(f'mdk4 {ifname} d -c {channel} -s 100', wait=False)
                self.btndeauth.set_label('Stop Deauther')
            else:
                display.set_text('[!]Select Interface and Channel')
        elif self.btndeauth.get_label() == 'Stop Deauther':
            self.run[2].kill()
            self.stop_monitor_mode(ifname, monmode)
            self.btndeauth.set_label('Start Deauther')

class CustomCommands(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.config_file = 'configuration.json'
        self.default_config = {"app_name": "Nethunter", "last_updated": str(datetime.datetime.now()), "commands_list": []}
        self.btnadd = self.builder.get_object('btn_ccmd_add')
        self.btnrm = self.builder.get_object('btn_ccmd_rm')

        self.btnadd.connect('clicked', self.add_command)
        self.btnrm.connect('clicked', lambda _: self.update_command(label='hello', delete=True))
        try:
            self.reload()
        except:
            self.write_config(self.default_config)
            self.reload()

    def read_config(self):
        with open(self.config_file, "r") as f:
            return json.load(f)
    
    def write_config(self, config):
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2)

    def reload(self):
        cmd_list = self.builder.get_object("ccmds_list")
        cmd_list.foreach(lambda child: cmd_list.remove(child))
        config = self.read_config()
        for c in config['commands_list']:
            label_txt = c['label']
            cmd = c['command']

            self.cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            label = Gtk.Label(label=label_txt)
            # label.set_property("margin", 5)
            label.set_ellipsize(Pango.EllipsizeMode.END)
            self.btnexec = Gtk.Button(label="EXECUTE")
            self.btnexec.set_property("margin", 5)
            self.btnexec.connect('clicked', self.execute_command, cmd)

            self.cmd_box.pack_start(label, False, False, 0)
            self.cmd_box.pack_end(self.btnexec, False, False, 0)

            cmd_list.pack_start(self.cmd_box, False, False, 0)
        cmd_list.show_all()

    def add_command(self, btn):
        get_inp = self.prompt()
        if get_inp is None:
            print('[!]Cancelled...')
            return 0
        elif get_inp == 1:
            print('[!]Invalid Input...')
            return 0

        config = self.read_config()
        new_entry = {'label': get_inp[0], "command": get_inp[1]}
        if not any(entry['label'] == new_entry['label'] for entry in config["commands_list"]):
            config["commands_list"].append(new_entry)
            self.write_config(config)
        else:
            print(f"An entry with name '{new_entry['label']}' already exists in the configuration.")
        self.write_config(config)
        self.reload()

    def update_command(self, label, new_cmd=None, delete=False):
        index = None
        config = self.read_config()
        for i, entry in enumerate(config["commands_list"]):
            if entry["label"] == label:
                index = i
                break
        if index is not None:
            if delete:
                del config["commands_list"][index]
            else:
                config["commands_list"][index]["command"] = new_cmd
            config["last_updated"] = str(datetime.datetime.now())
            self.write_config(config)
        self.reload()

    def execute_command(self, btn, cmd):
        self.get_output(cmd, shell=True, wait=False)[0]

    def run(self):
        pass

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
        CustomCommands(builder).run()

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
