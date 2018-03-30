#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
import signal
import subprocess
import os
from time import sleep

APPINDICATOR_ID = 'yubitoggle-applet'

icon_path = os.path.abspath('YubikeyEnabled.png')
indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon_path, appindicator.IndicatorCategory.SYSTEM_SERVICES)

def main():
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    currentState = isYubikeyEnabled()
    indicator.set_menu(build_menu(currentState))

    if not currentState:
        indicator.set_icon(os.path.abspath('YubikeyDisabled.png'))

    notify.init(APPINDICATOR_ID)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()

def build_menu(currentState):
    status = currentState
    menu = gtk.Menu()

    name = 'Disable Yubikey'
    goal_state = 0
    if not status:
        name = 'Enable Yubikey'
        goal_state = 1
    item_cmd = gtk.MenuItem(name)
    item_cmd.connect('activate', lambda x: toggle(goal_state))
    menu.append(item_cmd)

    item = gtk.MenuItem("Toggle")
    item.connect('activate', lambda x: toggle())
    menu.append(item)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu
 
def quit(source):
    gtk.main_quit()
    notify.uninit()

def toggle(goal_state=-1):
    env = dict(os.environ)
    env['DEBUG'] = "1"

    cmd = ['yubitoggle']
    if goal_state == 1:
        cmd.append('--on')
    elif goal_state == 0:
        cmd.append('--off')

    output = subprocess.check_output(cmd, env=env).decode('ascii', 'ignore')
    notify.Notification.new("Yubitoggle", output, None).show()

    currentState = isYubikeyEnabled()
    indicator.set_menu(build_menu(currentState))
    updateIcon(currentState)

def isYubikeyEnabled():
    output = subprocess.check_output(['yubitoggle', '--state']).decode('ascii', 'ignore')
    print("yubi state: " + output)
    return (int(output) == 1)

def updateIcon(currentState):
    icon = 'YubikeyEnabled.png' if currentState else 'YubikeyDisabled.png'
    indicator.set_icon(os.path.abspath(icon))

if __name__ == "__main__":
    main()
