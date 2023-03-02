import gi, time, subprocess
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gio, Notify
from bin import ducky


class MainWindow:
    def __init__(self):
        self.appname = 'USB Arsenal'
        self.usbarsenal = './bin/usbarsenal'
        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.mainWindow = self.builder.get_object('mainWindow')
        self.mainWindow.set_title(self.appname)
        Notify.init(self.appname)

        # ARSENAL
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
        self.setDefault()

        # DUCKY
        self.editor = self.builder.get_object('editor')
        self.btnOpen = self.builder.get_object('open')
        self.btnClear = self.builder.get_object('clear')
        self.btnSave = self.builder.get_object('save')
        self.btnInject = self.builder.get_object('inject')

        self.btnOpen.connect('clicked', self.openInEditor)
        self.btnClear.connect('clicked', self.clearEditor)
        self.btnSave.connect('clicked', self.save)
        self.btnInject.connect('clicked', self.inject)

        self.editor_buffer = self.editor.get_buffer()

        self.mainWindow.connect("destroy", Gtk.main_quit)
        self.mainWindow.show_all()
    
    # DUCKY FUNCTIONS
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

    def notification(self, msg):
        msg = Notify.Notification.new(self.appname, msg)
        msg.show()
    
    # ARSENAL FUNCTIONS
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
        
        self.setStatus(self.get_output(f'{self.usbarsenal} -s'))

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
                self.setStatus(self.get_output(f'{self.usbarsenal} -h'))
            elif data['function'] == 'teth':
                self.setStatus(self.get_output(f'{self.usbarsenal} -t'))
            elif data['function'] == 'mass':
                self.setStatus(self.get_output(f'{self.usbarsenal} -m {self.getMassStoragePath()}'))
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
            self.get_output(f'{self.usbarsenal} {ARGS}')

    def disable(self, btn):
        self.setStatus(self.get_output(f'{self.usbarsenal} -d'))

    def get_output(self, cmd):
        return str(subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0].decode())


win = MainWindow()
Gtk.main()