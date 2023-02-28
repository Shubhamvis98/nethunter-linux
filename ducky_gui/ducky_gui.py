import gi, time, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import ducky


class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('ducky.glade')
        self.mainWindow = self.builder.get_object('mainWindow')
        self.mainWindow.set_title("Ducky Injector")

        self.editor = self.builder.get_object('editor')
        self.btnClear = self.builder.get_object('clear')
        self.btnRun = self.builder.get_object('run')

        self.btnClear.connect('clicked', self.clearEditor)
        self.btnRun.connect('clicked', self.inject)

        self.mainWindow.connect("destroy", Gtk.main_quit)
        self.mainWindow.show_all()

    def clearEditor(self, btn):
        buffer = self.editor.get_buffer()
        buffer.set_text('')

    def inject(self, btn):
        buffer = self.editor.get_buffer()
        startIter, endIter = buffer.get_bounds()
        TMP = buffer.get_text(startIter, endIter, False)
        ducky.inject_raw(TMP)

win = MainWindow()
Gtk.main()
