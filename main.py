
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
import signal
import subprocess
import os


APPINDICATOR_ID = 'myappindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, 'whatever', appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    
    notify.init(APPINDICATOR_ID)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()

def build_menu():
    status = check_status()
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    name = 'Enable Yubikey'
    if not status:
        name = 'Disable Yubikey'

    item = gtk.MenuItem("Toggle")
    item.connect('activate', toggle)
    menu.append(item)

    menu.show_all()
    return menu
 
def quit(source):
    gtk.main_quit()
    notify.uninit()

def toggle(source):
    env = dict(os.environ)
    env['DEBUG'] = "1"
    output = subprocess.check_output(['yubitoggle'], env=env)
    notify.Notification.new("Yubitoggle", output, None).show()


def check_status():
    output = subprocess.check_output(['yubitoggle', '--status'])
    return (output == '1')

if __name__ == "__main__":
    main()
