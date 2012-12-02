#!/usr/bin/env python
# -*- coding: utf-8 -*-

#     This file is part of Bitacora. 
#     Please, read the "Copyright" and "LICENSE" variables for copyright advisement
#   (just below this line):

# Bitacora is a TODO Manager and a Binacle of TODOs
COPYRIGHT = "Copyright 2007-2009 Miguel Angel Garcia Martinez <miguelangel.garcia@gmail.com>"

LICENSE = """
    This file is part of Bitacora.

    Bitacora is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Bitacora is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Bitacora.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygtk
pygtk.require('2.0')
import gtk, gobject
import time
from calendarwindow import CalendarWindow

class ComboBoxCalendar(gtk.HBox):
    def __init__(self, name, format="%a %b %d %Y", parent_window=None):
        try:
            if not gobject.signal_lookup("on-change-cbcalendar", self):
                gobject.signal_new("on-change-cbcalendar",
                                   self,
                                   gobject.SIGNAL_RUN_LAST,
                                   gobject.TYPE_NONE,
                                   (float,))
        except:
            pass

        self.format = format
        self._name = name
        self.parent_window = parent_window

        gtk.HBox.__init__(self)

        self.entry = gtk.Entry()
        self.button = gtk.Button()
        arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_IN)
        self.button.add(arrow)
        
        self.entry.set_editable(False)
        self.button.connect("pressed", self.show_calendar)
        
        self.pack_start(self.entry, False, False)
        self.pack_start(self.button, False, False)

        self._value = 0
        
        self.direction = 'down'
        
        self.show_all()

    def do_change_calendar_window(self, calendarwindow, value):
        self.value = value
        if value == 0:
            self.entry.set_text('')
        else:
            self.entry.set_text(time.strftime(self.format, time.localtime(value)))
        self.emit("on-change-cbcalendar", value)

    def show_calendar(self, button):
        calendarbox = CalendarWindow(self._value, parent_window=self.parent_window)
        calendarbox.connect('on-change-calendar-window', self.do_change_calendar_window)
        
        entrypos = self.entry.get_allocation()
        parentpos = self.get_parent_window().get_position()

        if self.direction == 'up':
            calendarbox.move(parentpos[0] + entrypos.x,
                                  parentpos[1] + entrypos.y - calendarbox.get_size()[1])
        else:
            calendarbox.move(parentpos[0] + entrypos.x,
                                  parentpos[1] + entrypos.y + entrypos.height)


        calendarbox.run()
        


    def set_visibility(self, value):
        self.entry.set_visibility(value)

    def __set_value(self, value):
        if value == None:
            value = 0
        self._value = value
        if (value):
            self.entry.set_text(time.strftime(self.format, time.localtime(value)))
        else:
            self.entry.set_text("")


    def __get_value(self):
        return self._value

    value = property (__get_value, __set_value)


