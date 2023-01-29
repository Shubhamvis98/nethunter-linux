import gi, time, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('arsenal_gui.glade')
        self.mainWindow = self.builder.get_object('mainWindow')
        self.mainWindow.set_title("USB Arsenal")

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

        self.mainWindow.connect("destroy", Gtk.main_quit)
        self.setDefault()
        self.mainWindow.show_all()

    def getMassStoragePath(self):
        self.filechooser = self.builder.get_object('filechooser')
        return self.filechooser.get_filename()

    def setStatus(self, stsTxt):
        buffer = self.status.get_buffer()
        buffer.set_text(stsTxt)
    
    def getStatus(self):
        buffer = self.status.get_buffer()
        startIter, endIter = buffer.get_bounds()
        return(buffer.get_text(startIter, endIter, False))
    
    def setDefault(self):
        self.idVen.set_text('0x1D6B')
        self.idProd.set_text('0x0104')
        self.manufact.set_text('fossfrog')
        self.prod.set_text('HID Gadget')
        with open('/etc/machine-id', 'r')as macid:
            self.serialno.set_text(macid.read()[:-1])
        
        self.setStatus(self.get_output('./usbarsenal -s'))

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
                self.setStatus(self.get_output('./usbarsenal -h'))
            elif data['function'] == 'teth':
                self.setStatus(self.get_output('./usbarsenal -t'))
            elif data['function'] == 'mass':
                self.setStatus(self.get_output(f'./usbarsenal -m {self.getMassStoragePath()}'))
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
            self.get_output(f'./usbarsenal {ARGS}')


    def disable(self, btn):
        self.setStatus(self.get_output('./usbarsenal -d'))
    
    def get_output(self, cmd):
        return str(subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0].decode())

win = MainWindow()
Gtk.main()
