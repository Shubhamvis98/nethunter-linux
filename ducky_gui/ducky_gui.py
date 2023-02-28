import gi, time, subprocess
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gio, Notify
import ducky


class MainWindow:
    def __init__(self):
        self.appname = 'Ducky Injector'
        self.builder = Gtk.Builder()
        self.builder.add_from_file('ducky.glade')
        self.mainWindow = self.builder.get_object('mainWindow')
        self.mainWindow.set_title(self.appname)
        Notify.init(self.appname)

        self.editor = self.builder.get_object('editor')
        self.btnOpen = self.builder.get_object('open')
        self.btnClear = self.builder.get_object('clear')
        self.btnSave = self.builder.get_object('save')
        self.btnInject = self.builder.get_object('inject')

        self.btnOpen.connect('clicked', self.openInEditor)
        self.btnClear.connect('clicked', self.clearEditor)
        self.btnSave.connect('clicked', self.save)
        self.btnInject.connect('clicked', self.inject)

        self.buffer = self.editor.get_buffer()

        self.mainWindow.connect("destroy", Gtk.main_quit)
        self.mainWindow.show_all()
    
    def clearEditor(self, btn):
        buffer = self.editor.get_buffer()
        buffer.set_text('')

    def inject(self, btn):
        startIter, endIter = self.buffer.get_bounds()
        TMP = self.buffer.get_text(startIter, endIter, False)
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
                    self.buffer.set_text(f.read())
            except TypeError:
                buffer.set_text('Select File First...')
        filechooser.destroy()
    
    def save(self, btn):
        startIter, endIter = self.buffer.get_bounds()
        TMP = self.buffer.get_text(startIter, endIter, False)
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


win = MainWindow()
Gtk.main()