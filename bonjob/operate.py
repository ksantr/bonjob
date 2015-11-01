import logging
import os
from ConfigParser import SafeConfigParser, NoSectionError
from gi.repository import Gtk

logger = logging.getLogger(__name__)

class MenuSet(Gtk.Window):
    """ Menu Settings Class """

    def __init__(self):
        """ Load settings from config.ini file"""
        Gtk.Window.__init__(self, title="FileChooser Example")

        config = SafeConfigParser()
        self.confpath = self.get_path('config.ini')
        if not os.path.exists(self.confpath):
            logger.warning('Config file config.ini not found')
        config.read(self.confpath)
        self.pub_time = config.get('main', 'pub_time')
        self.short_break = config.get('main', 'short_break')
        self.maxshort_break = config.get('main', 'maxshort_break')
        self.long_break = config.get('main', 'long_break')
        self.song_switch = config.get('main', 'song_switch')
        self.songs_switch = config.get('main', 'songs_switch')
        self.filename = config.get('main', 'filename')
        self.foldername = config.get('main', 'foldername')
        self.tooltip_switch = config.get('main', 'tooltip_switch')
        self.timer_switch = config.get('main', 'timer_switch')

    def get_path(self, fname):
        """ Get absolute path of file """
        dirname = os.path.dirname(__file__)
        real = os.path.join(dirname, fname)
        abs_path = os.path.abspath(real)
        return abs_path

    def update_config(self):
        """ Save current settings to config.ini """
        config = SafeConfigParser()
        try:
            config.set('main', 'pub_time', str(self.pub_time))
        except NoSectionError as e:
            config.add_section('main')
            
        config.set('main', 'pub_time', str(self.pub_time))
        config.set('main', 'short_break', str(self.short_break))
        config.set('main', 'maxshort_break', str(self.maxshort_break))
        config.set('main', 'long_break', str(self.long_break))
        config.set('main', 'song_switch', str(self.song_switch))
        config.set('main', 'songs_switch', str(self.songs_switch))
        config.set('main', 'filename', self.filename)
        config.set('main', 'foldername', self.foldername)
        config.set('main', 'tooltip_switch', str(self.tooltip_switch))
        config.set('main', 'timer_switch', str(self.timer_switch))

        try:
            config.write(open(self.confpath, 'w'))
        except IOError as e:
            logger.warning(e)

    def song_switch_click(self, switch, gparam):
        if switch.get_active():
            state = "on"
        else:
            state = "off"
        self.song_switch = state
        self.update_config()
        logger.info("Song Switch was turned %s" % state)

    def songs_switch_click(self, switch, gparam):
        if switch.get_active():
            state = "on"
        else:
            state = "off"
        self.songs_switch = state
        self.update_config()
        logger.info("Songs Switch was turned %s" % state)

    def tooltip_switch_click(self, switch, gparam):
        if switch.get_active():
            state = "on"
        else:
            state = "off"
        self.tooltip_switch = state
        self.update_config()
        logger.info("Tooltip Switch was turned %s" % state)

    def timer_switch_click(self, switch, gparam):
        if switch.get_active():
            state = "on"
        else:
            state = "off"
        self.timer_switch = state
        self.update_config()
        logger.info("Timer Switch was turned %s" % state)

    def pub_time_click(self, switch):
        self.pub_time = switch.get_value()
        self.update_config()
        logger.info("PubTime Switch was turned to %s" % self.pub_time)

    def short_break_click(self, switch):
        self.short_break = switch.get_value()
        self.update_config()
        logger.info("ShortTime Switch was turned to %s" % self.short_break)

    def maxshort_break_click(self, switch):
        self.maxshort_break = switch.get_value()
        self.update_config()
        logger.info("MaxShort Switch was turned to %s" % self.maxshort_break)

    def long_break_click(self, switch):
        self.long_break = switch.get_value()
        self.update_config()
        logger.info("LongBreak Switch was turned to %s" % self.long_break)

    ##################################
    ##### File chooser's methods #####
    ##################################

    def add_filters(self, dialog):
        filter_mp3 = Gtk.FileFilter()
        filter_mp3.set_name("Audio")
        filter_mp3.add_mime_type("audio/mpeg")
        filter_mp3.add_mime_type("audio/mp3")
        dialog.add_filter(filter_mp3)

    def on_file_click(self, widget, label):
        """ Select File """
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            logger.info("Open clicked")
            logger.info("File selected: " + dialog.get_filename())
            self.filename = dialog.get_filename()
            label.set_text(self.filename)
            self.update_config()
        elif response == Gtk.ResponseType.CANCEL:
            logger.info("Cancel clicked")

        dialog.destroy()

    def on_folder_click(self, widget, label):
        """ Select Folder """
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            logger.info("Select clicked")
            logger.info("Folder selected: " + dialog.get_filename())
            self.foldername = dialog.get_filename()
            label.set_text(self.foldername)
            self.update_config()
        elif response == Gtk.ResponseType.CANCEL:
            logger.info("Cancel clicked")

        dialog.destroy()
