#!/usr/local/bin/python
#####################################################################
# Copyright (c) 2015, GhostBSD. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistribution's of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistribution's in binary form must reproduce the above
#    copyright notice,this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# 3. Neither then name of GhostBSD nor the names of its
#    contributors maybe used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES(INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#####################################################################

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
import pexpect
from subprocess import Popen, PIPE
from subprocess import Popen, PIPE
import sys
from time import sleep
sys.path.append('/usr/home/ericbsd/gbsudo/')

class askPassword():
    def delete(self, widget, event=None):
        Gtk.main_quit()
        return False

    def __init__(self, arg):
        self.trytimes = 0
        self.arg = arg
        self.window = Gtk.Window()
        #self.window.set_size_request(700, 500)
        #self.window.set_resizable(False)
        self.window.connect("delete_event", self.delete)
        self.window.set_title("Sudo Password")
        self.window.set_border_width(0)
        #self.window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = Gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # Title
        Title = Gtk.Label("<b><span size='x-large'>Enter you password:</span></b>")
        Title.set_use_markup(True)
        box2.pack_start(Title, False, False, 0)
        # chose Disk
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.show()
        # password
        self.passwd_label = Gtk.Label("Password:")
        self.passwordentry = Gtk.Entry()
        self.passwordentry.set_visibility(False)
        self.passwordentry.connect('activate', self.setpassword)
        grid.attach(self.passwd_label, 0, 1, 1, 1)
        grid.attach(self.passwordentry, 3, 1, 2, 1)
        box2.pack_start(grid, True, True, 10)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, False, 0)
        box2.show()
        self.table = Gtk.Table(1, 6, True)
        self.button2 = Gtk.Button(label='Cancel')
        self.button2.connect("clicked", self.delete)
        self.table.attach(self.button2, 4, 5, 0, 1)
        self.button2.show()
        self.button3 = Gtk.Button(label='Ok')
        self.button3.connect("clicked", self.setpassword)
        self.table.attach(self.button3, 5, 6, 0, 1)
        self.button3.show()
        self.table.set_col_spacings(5)
        self.table.show()
        # Add button
        box2.pack_start(self.table,True, True, 5)
        self.window.show_all()
        Gtk.main()

    def setpassword(self, widget):
        self.window.hide()
        trytimes += 1

        if trytimes <= 3:
            self.password = self.passwordentry.get_text()
            GLib.idle_add(self.sudopasswd, self.arg, self.password)
        else:
            Gtk.main_quit()

    def passwordAutentification(self, arg, psswrd):
        #self.window.hide()
        sudocomand = 'sudo ' + arg
        sudochild = pexpect.spawn(sudocomand)
        sudochild.expect(['Password:'])
        sudochild.sendline(psswrd)
        i = sudochild.expect(['is not in the sudoers file.', 'Password:', pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            print 0
            sudochild.kill(0)
            Gtk.main_quit()
        elif i == 1:
            print 1
            sudochild.kill(0)
            self.passwordentry.set_text("")
        elif i == 2:
            print 2
            sudochild.interact()
            Gtk.main_quit()
        elif i == 3:
            self.window.hide()
            sudochild.interact()
            Gtk.main_quit()

    def sudopasswd(self, arg, psswrd):
        command = arg.split()
        p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
        sudo_prompt = p.communicate(psswrd + '\n')[1]
        if "incorrect password" in sudo_prompt:
            print('incorrect password')
            self.passwordentry.set_text("")
            self.window.show_all()
        elif "is not in the sudoers" in sudo_prompt:
            print('user not in the sudoers')
            Gtk.main_quit()
        else:
            print('it work')
            Gtk.main_quit()


if len(sys.argv) == 2:
    askPassword(sys.argv[1])
else:
    print "need argument"
