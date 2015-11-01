import logging
import mimetypes
import os
import subprocess


logger = logging.getLogger(__name__)


class Player:
    """
    Audio player for Bonjob.
    This player uses the Audacious player.
    init with dafault song value
    """
    def __init__(self):
        # init with dafault sound
        dirname = os.path.dirname(__file__)
        real_path = os.path.join(dirname, 'sounds', 'eyes.mp3')
        self.default_sound = os.path.abspath(real_path)

    def check_file(self, sound):
        """ Check file existence and mime type """
        if not os.path.exists(sound):
            logger.warning('%s not found, using default' % sound)
            return self.default_sound
        else:
            mime = mimetypes.guess_type(sound)
            if not mime[0] == 'audio/mpeg':
                logger.warning('bad mime type %s, using default' % sound)
                return self.default_sound
            else:
                return sound

    def play_single(self, sound):
        """ Single sound player """
        sound = self.check_file(sound)
        subprocess.Popen(["audacious", sound, "-phE"])
        logger.info('Audio single sound %s started' % sound)

    def play_list(self, dirname):
        """ Player of sounds from arg dirname """
        files = []
        for dirpath, dirname, filename in os.walk(dirname):
            for f in filename:
                files.append(os.path.join(dirpath, f))

        playlist = set(map(self.check_file, files))

        tasklist = ['audacious', '-phE']
        tasklist.extend(playlist)

        subprocess.Popen(tasklist)
        logger.info('Audio play list has started')

    def kill(self):
        """ Audacious killer """
        subprocess.Popen(["pkill", "audacious"])
        logger.info('audacious has killed')


    def pause(self):
        """ Pause/Resume pasused sound in audacious """
        subprocess.Popen(["audacious", "--pause"])
        logger.info('Audio module has paused')

if __name__ == '__main__':
    logging.basicConfig(format=('%(levelname)s - %(message)s'),
                        level=logging.INFO,
                        datefmt='%y/%m/%d %H-%M')

    p = Player()
    p.play_list('/tmp/test')
