#!/usr/bin/python3
# Author Shubham Vishwakarma
# git/twitter: ShubhamVis98

import gi, os, threading, subprocess, psutil, random, json, datetime
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

    def set_app_theme(theme_name, isdark=False):
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-theme-name", theme_name)
        settings.set_property("gtk-application-prefer-dark-theme", isdark)

    def terminate_processes(proc_name, params):
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] == proc_name and params in str(proc.info['cmdline']):
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.terminate()
                except psutil.NoSuchProcess as e:
                    print(f"Error terminating process {proc.info['pid']}: {e}")

    def ls_btiface():
        result = subprocess.run(['hciconfig'], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()

        interfaces = []
        for line in output_lines:
            if line.startswith('hci'):
                interface_name = line.split(':')[0]
                interfaces.append(interface_name)

        return interfaces

class AppDetails:
    name = 'NetHunter'
    version = '1.9'
    desc = "A Clone of Android's NetHunter for GNU/Linux Phones"
    dev = 'Shubham Vishwakarma'
    install_path = '/usr/lib/nethunter'
    # install_path = '.'
    ui = f'{install_path}/nethunter.ui'
    applogo = 'in.fossfrog.nethunter'
    config_path = f"{os.path.expanduser('~')}/.config/nethunter"
    config_file = f'{config_path}/configuration.json'

class AboutScreen(Gtk.Window):
    def __init__(self):
        super().__init__()
        builder = Gtk.Builder()
        builder.add_from_file(AppDetails.ui)

        # Get IDs from UI file
        self.about_win = builder.get_object('about_window')
        app_logo = builder.get_object('app_logo')
        app_name_ver = builder.get_object('app_name_ver')
        app_desc = builder.get_object('app_desc_about')
        app_dev = builder.get_object('app_dev')
        btn_about_close = builder.get_object('btn_about_close')

        # Set logo
        icon_theme = Gtk.IconTheme.get_default()
        pixbuf = icon_theme.load_icon(AppDetails.applogo, 150, 0)
        app_logo.set_from_pixbuf(pixbuf)

        # Set app details
        app_name_ver.set_markup(f'<b>{AppDetails.name} {AppDetails.version}</b>')
        app_desc.set_markup(f'{AppDetails.desc}')
        app_dev.set_markup(f'Copyright © 2024 {AppDetails.dev}')

        btn_about_close.connect('clicked', self.on_close_clicked)

        self.about_win.set_title('About')
        self.add(self.about_win)
        self.about_win.show()

    def on_close_clicked(self, widget):
        self.destroy()

class Home(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.app_name = self.builder.get_object('app_name')
        self.app_version = self.builder.get_object('app_version')
        self.app_desc = self.builder.get_object('app_desc')
        self.app_warn = self.builder.get_object('app_warn')
        self.btn_main_quit = self.builder.get_object('btn_main_quit')
        self.btn_main_quit.connect('clicked', Gtk.main_quit)
        self.builder.get_object('btn_about').connect('clicked', self.show_about)

        self.app_name.set_label('NETHUNTER')
        self.app_version.set_label(f'{AppDetails.version}\nby @ShubhamVis98')
        self.app_desc.set_label("\nFEATURES:\n- USB Arsenal\n- HID, Mass Storage and USB Tethering (BadUSB)\n- USB Ducky\n- MAC Changer\n- Deauther\n- Custom Commands\n- BadBT (Bluetooth Ducky)\n\ngit/twitter: ShubhamVis98\nyoutube: fossfrog\n")
        self.app_warn.set_label("!!!WARNING!!!\nDON'T MISUSE YOUR SUPERPOWERS")
        Functions.set_app_theme("Adwaita", True)
    
    def run(self):
        pass

    def show_about(self, widget=None):
        AboutScreen()

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
        self.btlabel = self.builder.get_object('ducky_l')

        self.editor_buffer = self.editor.get_buffer()

    def run(self):
        pass

    def clearEditor(self, btn):
        self.editor_buffer.set_text('')

    def inject(self, btn):
        startIter, endIter = self.editor_buffer.get_bounds()
        TMP = self.editor_buffer.get_text(startIter, endIter, False)
        if self.btlabel.get_text() == 'BT Ducky':
            dtmp = self.get_output('mktemp')[0].strip()
            with open(dtmp, 'w') as _dtmp:
                _dtmp.write(TMP)
            self.get_output(f'python3 badbt/ducky.py -d {dtmp}')[1]
            os.remove(dtmp)
        else:
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

class BadBT(Functions):
    def __init__(self, builder):
        self.builder = builder
        self.btiface = self.builder.get_object('btiface')
        self.btname = self.builder.get_object('btname')
        self.btsrvswitch = self.builder.get_object('btsrvswitch')
        self.btdswitch = self.builder.get_object('btdswitch')
        self.btstatus = self.builder.get_object('badbt_status')
        
        self.btstatus_buffer = self.btstatus.get_buffer()
        self.btsrvswitch.connect("state-set", self.btserver_state)
        self.btdswitch.connect("state-set", self.btdswitch_state)

        self.btlabel = self.builder.get_object('ducky_l')
    
    def btserver_state(self, switch, state):
        btname = 'fossfrog' if self.btname.get_text().strip() == '' else self.btname.get_text()
        btiface = self.btiface.get_active_text()
        if btiface == 'None':
            self.setStatus('[!]Interface not found')
            return

        srvcmd = threading.Thread(target=lambda: self.get_output(f'python3 badbt/btk_server.py -n {btname} -i {btiface}'))

        if state and not srvcmd.is_alive():
            srvcmd.start()
            self.setStatus(f'[+]Server Started...\n\tBT NAME: {btname}\n\tIFACE: {btiface}')
        elif not state:
            Functions.terminate_processes('python3', 'btk_server.py')
            self.setStatus('[-]Server Stopped.')

    def btdswitch_state(self, switch, state):
        if state:
            self.btlabel.set_text('BT Ducky')
            self.setStatus('[+]BT Ducky Enabled')
        else:
            self.btlabel.set_text('Ducky')
            self.setStatus('[+]Back to USB Ducky')

    def setStatus(self, stsTxt, clear=False):
        if clear:
            tmp = stsTxt
        else:
            tmp = self.getStatus() + '\n' + stsTxt
        self.btstatus_buffer.set_text(tmp)
    
    def getStatus(self):
        startIter, endIter = self.btstatus_buffer.get_bounds()
        return(self.btstatus_buffer.get_text(startIter, endIter, False))

    def chkbadbt(self):
        if not os.path.exists('badbt'):
            self.setStatus('[!]BadBT missing.\n[+]Cloning BadBT...')
            run = self.get_output('git clone https://github.com/shubhamvis98/badbt')
            if run[1] != 0:
                self.setStatus('[!]Failed to Clone. Reopen Nethunter with working internet connection.')
            else:
                self.setStatus('[+]Clone Completed.')

    def run(self):
        threading.Thread(target=self.chkbadbt).start()
        btifaces = Functions.ls_btiface()
        if len(btifaces) != 0:
            self.btiface.remove_all()
            for i in btifaces:
                self.btiface.append_text(i)
            self.btiface.set_active(0)
            self.setStatus('[+]Interface List Loaded')

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
            out = self.get_output(f"iwlist {ifname} scanning | grep -E 'ESSID|Frequency' | tac", shell=True)
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
        gear_icon = Gio.ThemedIcon(name="preferences-system-symbolic")
        
        for c in config['commands_list']:
            label_txt = c['label']
            cmd = c['command']

            cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            label = Gtk.Label(label=label_txt, margin=5)
            label.set_ellipsize(Pango.EllipsizeMode.END)
            btnedit = Gtk.Button(margin=5)
            btnedit.set_image(Gtk.Image.new_from_gicon(gear_icon, Gtk.IconSize.BUTTON))
            btnexec = Gtk.Button(label="EXECUTE", margin=5)

            btnedit.connect('clicked', self.update_command, [label_txt, cmd])
            btnexec.connect('clicked', self.execute_command, cmd)

            cmd_box.pack_start(label, False, False, 0)
            cmd_box.pack_end(btnexec, False, False, 0)
            cmd_box.pack_end(btnedit, False, False, 0)

            cmd_list.pack_start(cmd_box, False, False, 0)
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
        Gtk.Window.set_default_icon_name(AppDetails.applogo)

    def do_activate(self):
        appname = 'NetHunter'
        builder = Gtk.Builder()
        builder.add_from_file("nethunter.ui")

        # Initialize Functions
        Home(builder).run()
        Arsenal(builder).run()
        Ducky(builder).run()
        BadBT(builder).run()
        MACChanger(builder).run()
        Deauther(builder).run()
        CustomCommands(builder).run()

        # Get The main window from the glade file
        window = builder.get_object("nh_main")
        window.set_title(appname)
        Notify.init(appname)

        # Show the window
        # window.connect("destroy", Gtk.main_quit)
        window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


nh = NHGUI().run(None)
Gtk.main()
