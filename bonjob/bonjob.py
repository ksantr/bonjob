#!/usr/bin/env python
import logging
import os
import subprocess
from gi.repository import Gtk
from gi.repository import AppIndicator3 as app3
from gi.repository import GObject
from audio import Player
from operate import MenuSet
import prefs


logger = logging.getLogger(__name__)
logformat = '%(asctime)-12s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logformat,
                    datefmt='%y/%m/%d %H-%M',
                    level=logging.INFO)

class Bonjob:
    def __init__(self):
        logger.info('Bonjob started')

        # Menu indicator
        self.ind = app3.Indicator.new('Bonjob',
                                      'Bonjob',
                                      app3.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(app3.IndicatorStatus.ACTIVE)
        self.state = 'idle'
        self.ind.set_icon(self.imgpath())

        # init modules
        self.player = Player()
        self.mset = MenuSet()
        # Counter for timer
        self.break_counter = 0

        #####################
        ##### GUI setup #####
        #####################

        self.menu = Gtk.Menu()
        self.item = Gtk.MenuItem('Start')
        self.item.connect('activate', self.control_click)
        self.item.show()
        self.menu.append(self.item)
        # Separator
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)
        # Settings
        item2 = Gtk.MenuItem('Settings')
        item2.connect('activate', self.pref, None)
        item2.show()
        self.menu.append(item2)
        # A quit item
        item3 = Gtk.MenuItem('Quit')
        item3.connect('activate', self.quit, None)
        item3.show()
        self.menu.append(item3)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def quit(self, widget, args):
        """ Stop all and quit program """
        # Exit timer
        self.break_timer = True
        # Kill music
        self.player.kill()
        # Exit GUI
        Gtk.main_quit()

    def imgpath(self):
        """ Get absolute path for current state img """
        dirname = os.path.dirname(__file__)
        real = os.path.join(dirname, 'images', self.state + '.png')
        abs_path = os.path.abspath(real)

        return abs_path

    def change_icon(self):
        """ Change menu app icon """
        icon_path = self.imgpath()
        self.ind.set_icon(icon_path)

    def pref(self, *args):
        """ Open window with settings """
        win = prefs.SettingsWindow()
        win.show_all()
        prefs.Gtk.main()

        # Get object with changed settings
        self.mset = MenuSet()

    def control_click(self, *args):
        """ Start/Stop menu click """

        logger.info('Leave %s state' % self.state)

        if self.state == 'idle':
            self.item.get_child().set_text('Stop')
            self.break_timer = False
            self.timer()
        elif self.state == 'break':
            self.item.get_child().set_text('Start')
            self.break_timer = True
            self.state = 'idle'
            self.notify('Stop')
            logger.info('Start %s state' % self.state)
        else:
            self.item.get_child().set_text('Start')
            self.break_timer = True
            self.state = 'idle'
            self.notify('Stop')
            logger.info('Start %s state' % self.state)

    def timer(self):
        """
        Main status control method
        based on time settings from config.ini file.
        break_counter - counter of the short breaks
        """
        # Exit if stopped
        if self.break_timer is True:
            return

        if self.state == 'working':
            self.state = 'break'
            logger.info('Start %s state' % self.state)

            if self.break_counter == float(self.mset.maxshort_break):
                self.break_counter = 0
                self.notify('Time for long break')
                time = float(self.mset.long_break) * 10000
                GObject.timeout_add(time, self.timer)
            else:
                self.break_counter += 1
                self.notify('Time for short break')
                time = float(self.mset.short_break) * 10000
                GObject.timeout_add(time, self.timer)
        else:
            self.state = 'working'
            logger.info('Start %s state' % self.state)
            self.notify('Time to work')
            time = float(self.mset.pub_time) * 10000
            GObject.timeout_add(time, self.timer)

    def notify(self, message):
        """
        Notify about timeout signals.
        Change icon, play mausic, show message.
        """
        # Change menu icon
        self.change_icon()

        if self.state == 'break':
            # Play single file
            if self.mset.song_switch == 'on':
                self.player.play_single(self.mset.filename)

            # Play files from folder
            if self.mset.songs_switch == 'on':
                self.player.play_list(self.mset.foldername)
        else:
            if self.mset.song_switch == 'on' or self.mset.songs_switch == 'on':
                self.player.kill()

        # Show window message
        if self.mset.tooltip_switch == 'on':
            task = 'notify-send -u normal "%s" -i %s' % (message, self.imgpath())
            subprocess.Popen(task, shell=True)

    def main(self):
        Gtk.main()

if __name__ == '__main__':
    app = Bonjob()
    app.main()
