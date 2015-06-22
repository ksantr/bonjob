import logging
from gi.repository import Gtk
from operate import MenuSet

logger = logging.getLogger(__name__)

class SettingsWindow(Gtk.Window):
    """ Creator of window with settings """
    def __init__(self):
        Gtk.Window.__init__(self, title="Bonjob settings")
        self.set_border_width(15)
        self.set_position(Gtk.WindowPosition.CENTER)
        #self.set_position(Gtk.WindowPosition.MOUSE)
        mset = MenuSet()

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        hbox.connect("destroy", self.destroy, None)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(listbox, True, True, 0)

        #########################
        ##### Time settings #####
        #########################

        title = '<span font="12"><b>Timer</b></span>'
        label = self.add_label(title)
        row = self.add_row(label)
        listbox.add(row)

        ##### Bonjob duration #####

        label = self.add_label('Work duration')
        spin = self.add_spin(mset.pub_time, mset.pub_time_click)
        box = self.hBox(label, spin)
        row = self.add_row(box)
        listbox.add(row)

        ##### Short break #####

        label = self.add_label('Short break duration')
        spin = self.add_spin(mset.short_break, mset.short_break_click)
        box = self.hBox(label, spin)
        row = self.add_row(box)
        listbox.add(row)

        ##### Max short breaks #####

        label = self.add_label('Max short breaks')
        spin = self.add_spin(mset.maxshort_break, mset.maxshort_break_click)
        box = self.hBox(label, spin)
        row = self.add_row(box)
        listbox.add(row)

        ##### Long break #####

        label = self.add_label('Long break duration')
        spin = self.add_spin(mset.long_break, mset.long_break_click)
        box = self.hBox(label, spin)
        row = self.add_row(box)
        listbox.add(row)

        ##########################
        ##### Sound Settings #####
        ##########################

        title = '<span font="12"><b>Sound</b></span>'
        label = self.add_label(title)
        row = self.add_row(label)
        listbox.add(row)

        ##### Play single file #####

        label = self.add_label('Play single file')
        spin = self.add_switch(mset.song_switch, mset.song_switch_click)
        box = self.hBox(label, spin)
        row = self.add_row(box)
        listbox.add(row)

        ##### Choose file #####

        label = self.add_label(mset.filename)
        button1 = Gtk.Button("Choose File")
        button1.connect("clicked", mset.on_file_click, label)
        box = self.hBox(label, button1)
        row = self.add_row(box)
        listbox.add(row)

        ##### Play random file #####

        label = self.add_label('Play random file')
        spin = self.add_switch(mset.songs_switch, mset.songs_switch_click)
        box = self.hBox(label, spin)
        row = self.add_row(box)
        listbox.add(row)

        ##### Choose folder #####

        label = self.add_label(mset.foldername)
        button2 = Gtk.Button("Choose Folder")
        button2.connect("clicked", mset.on_folder_click, label)
        box = self.hBox(label, button2)
        row = self.add_row(box)
        listbox.add(row)

        ###############################
        ##### Additional Settings #####
        ###############################

        title = '<span font="12"><b>Additional</b></span>'
        label = self.add_label(title)
        row = self.add_row(label)
        listbox.add(row)

        ##### Show tooltip #####

        label = self.add_label('Show tooltip message')
        spin = self.add_switch(mset.tooltip_switch, mset.tooltip_switch_click)
        box = self.hBox(label, spin)
        row = self.add_row(box)
        listbox.add(row)

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def add_row(self, *widgets):
        """ Create new row, add widgets """
        row = Gtk.ListBoxRow()

        for widget in widgets:
            row.add(widget)

        return row

    def vBox(self, *widgets):
        """ Create new vertical box, add widgets"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        for widget in widgets:
            box.pack_start(widget, True, False, 0)

        return box

    def add_label(self, markup):
        """ label creation function """
        label = Gtk.Label()
        label.set_markup(markup)

        return label

    def add_spin(self, value, callback=False):
        """ Create SpinButton with callback function """
        if callback is False:
            raise AttributeError('callback error in self.add_spin')

        adjustment = Gtk.Adjustment(float(value), 0, 100, 1, 10, 0)
        spinbutton = Gtk.SpinButton()
        spinbutton.set_numeric(True)
        spinbutton.set_adjustment(adjustment)
        spinbutton.connect("value-changed", callback)

        return spinbutton

    def add_switch(self, status, callback=False):
        """ Create switch button with callback """
        if callback is False:
            raise AttributeError('callback error in self.add_switch')

        switch = Gtk.Switch()
        switch.connect("notify::active", callback)

        if status == 'on':
            switch.set_active(True)

        return switch

    def hBox(self, label=False, *widgets):
        """
        Create horizontal Gtk.Box with label at start and
        widgets at the end.
        """
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box.pack_start(label, False, False, 10)

        for widget in widgets:
            box.pack_end(widget, False, False, 5)

        return box


if __name__ == '__main__':
    win = SettingsWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    #win.hide()
    Gtk.main()
