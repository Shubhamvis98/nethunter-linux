#!/usr/bin/python3
# Author Shubham Vishwakarma
# git/twitter: ShubhamVis98

import gi, subprocess, psutil, random, json, datetime
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gio, Pango, Notify
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
    
    def prompt(self, label=None, cmd=None):
        title = 'Update Command' if label else 'Add Command'
        label = label if label is not None else 'Label'
        cmd = cmd if cmd is not None else 'Command'
        dialog = Gtk.Dialog(title)
        if title == 'Update Command':
            dialog.add_buttons(
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_DELETE,
                Gtk.ResponseType.NO
            )
        else:
            dialog.add_buttons(
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
            )

        box_label = Gtk.Entry(text=label, margin=5)
        box_cmd = Gtk.Entry(text=cmd, margin=5)
        dialog.vbox.pack_start(box_label, True, True, 0)
        dialog.vbox.pack_start(box_cmd, True, True, 0)
        dialog.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            label = box_label.get_text()
            cmd = box_cmd.get_text()
            ret = [label, cmd] if (label and cmd) != '' else None
        elif response == Gtk.ResponseType.CANCEL:
            ret = False
        elif response == Gtk.ResponseType.NO:
            self.delete_command(None, label)
            ret = None

        dialog.destroy()
        return ret

class Home(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.app_name = self.builder.get_object('app_name')
        self.app_version = self.builder.get_object('app_version')
        self.app_desc = self.builder.get_object('app_desc')
        self.app_warn = self.builder.get_object('app_warn')

        self.app_name.set_label('NETHUNTER')
        self.app_version.set_label('v1.4-alpha\nby @ShubhamVis98')
        self.app_desc.set_label("\nFEATURES:\n- USB Arsenal\n- HID, Mass Storage and USB Tethering\n- Ducky implemented but maybe some keys won't work\n- MAC Changer\n- Deauther\n- Custom Commands\n\ngit/twitter: ShubhamVis98\nyoutube: fossfrog\n")
        self.app_warn.set_label("!!!WARNING!!!\nDON'T MISUSE YOUR SUPERPOWERS")
    
    def run(self):
        pass

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

        self.btnadd.connect('clicked', self.add_command)
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
        cmd_list.show_all()
        gear_icon = Gtk.Image.new_from_icon_name("preferences-system-symbolic", Gtk.IconSize.BUTTON)

        for c in config['commands_list']:
            label_txt = c['label']
            cmd = c['command']

            self.cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            label = Gtk.Label(label=label_txt, margin=5)
            label.set_ellipsize(Pango.EllipsizeMode.END)
            self.btnedit = Gtk.Button(image=gear_icon, margin=5)
            self.btnexec = Gtk.Button(label="EXECUTE", margin=5)

            self.btnedit.connect('clicked', self.update_command, [label_txt, cmd])
            self.btnexec.connect('clicked', self.execute_command, cmd)

            self.cmd_box.pack_start(label, False, False, 0)
            self.cmd_box.pack_end(self.btnexec, False, False, 0)
            self.cmd_box.pack_end(self.btnedit, False, False, 0)

            cmd_list.pack_start(self.cmd_box, False, False, 0)
        cmd_list.show_all()

    def add_command(self, btn):
        get_inp = self.prompt()
        if get_inp is False:
            print('[!]Cancelled...')
            return
        elif get_inp is None:
            print('[!]Invalid Input...')
            return

        config = self.read_config()
        new_entry = {'label': get_inp[0], "command": get_inp[1]}
        if not any(entry['label'] == new_entry['label'] for entry in config["commands_list"]):
            config["commands_list"].append(new_entry)
            self.write_config(config)
        else:
            self.notification(f"{new_entry['label']}: [!]Already Exists")
        self.write_config(config)
        self.reload()

    def delete_command(self, btn, label):
        index = None
        config = self.read_config()
        for i, entry in enumerate(config["commands_list"]):
            if entry["label"] == label:
                index = i
                break
        if index is not None:
            del config["commands_list"][index]
            config["last_updated"] = str(datetime.datetime.now())
            self.write_config(config)
        self.reload()

    def update_command(self, btn, entry):
        label = entry[0]
        cmd = entry[1]
        try:
            new_label, new_cmd = self.prompt(entry[0], entry[1])
        except:
            return
        index = None
        config = self.read_config()
        for i, entry in enumerate(config["commands_list"]):
            if entry["label"] == label:
                index = i
                break
        if index is not None:
            config["commands_list"][index]["label"] = new_label
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
        Home(builder).run()
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
