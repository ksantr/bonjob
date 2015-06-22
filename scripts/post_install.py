import logging
import os
import re
from shutil import copyfile
from ConfigParser import SafeConfigParser

logger = logging.getLogger(__name__)
logformat = '%(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logformat, level=logging.INFO)

class AppSetup:
    """ Bonjob installation class """
    def __init__(self):
        self.audacious_reconf()
        self.create_config()
        self.put_icon()

    def put_icon(self):
        """ Copy icon to .local/share/icons/ """
        dest_icon_path = self.get_abspath('.local/share/icons/bonjob.png')
        joined = os.path.join(self.get_app_path(), 'images/working.png')
        source_icon_path = os.path.abspath(joined)
        try:
            copyfile(source_icon_path, dest_icon_path)
        except IOError as e:
            logger.info('[-] Copy bonjob.png icon error %s' % e)
        else:
            logger.info('[+] Copy bonjop.png icon to %s' % dest_icon_path)

    def get_abspath(self, name):
        """ Get absolute path of file """
        dirname = os.path.dirname(__file__)
        real = os.path.join(dirname, os.environ['HOME'], name)
        abs_path = os.path.abspath(real)
        return abs_path

    def get_app_path(self):
        # Get directory with bonjob.py
        dirname = os.path.dirname(__file__)
        app_path = os.path.abspath(os.path.join(dirname, '..', 'bonjob'))
        return app_path

    def audacious_reconf(self):
        """ Reconfigure audacious config """
        aconf = self.get_abspath('.config/audacious/config')
        try:
            with open(aconf, 'r') as f:
                conf = f.read()
        except IOError:
            logger.warning('[-] Config read error: %s' % aconf)
            try:
                with open(aconf, 'a+') as f:
                    conf = '[audacious]\nrepeat=TRUE\nshuffle=TRUE'
                    f.write(conf)
            except IOError:
                logger.warning('[-] Config write error: %s' % aconf)
        else:
            conf = re.sub('repeat=FALSE', 'repeat=TRUE', conf)
            conf = re.sub('shuffle=FALSE', 'shuffle=TRUE', conf)

            with open(aconf, 'w') as f:
                f.write(conf)

            logger.info('[+] Write audacious config in %s' % aconf)

    def create_config(self):
        """ Save current settings to config.ini """

        config = SafeConfigParser()
        config.optionxform = str
        config.add_section('Desktop Entry')
        config.set('Desktop Entry', 'Encoding', 'UTF-8')
        config.set('Desktop Entry', 'Version', '1.0')
        config.set('Desktop Entry', 'Type', 'Application')
        config.set('Desktop Entry', 'Name', 'Bonjob')
        config.set('Desktop Entry', 'Icon', 'bonjob.png')
        config.set('Desktop Entry', 'Path', self.get_app_path())
        config.set('Desktop Entry', 'Exec', 'python bonjob.py')
        config.set('Desktop Entry', 'StartupNotify', 'false')
        config.set('Desktop Entry', 'X-UnityGenerated', 'true')
        #config.set('Desktop Entry', 'OnlyShowIn', 'Unity')

        try:
            conf_path = self.get_abspath('.local/share/applications/bonjob.desktop')
            config.write(open(conf_path, 'w'))
        except IOError as e:
            logger.warning('[-] %s' % e)
        else:
            logger.info('[+] Create bonjob.desktop in %s' % conf_path)

if __name__ == '__main__':
    setup = AppSetup()
    '''
    setup.audacious_reconf()
    setup.create_config()
    setup.put_icon()
    '''
