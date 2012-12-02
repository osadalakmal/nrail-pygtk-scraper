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

import time
import gtk, gobject


class CalendarWindow(gtk.Dialog):
    def __init__(self, initial_value=0, parent_window=None):
        gtk.Dialog.__init__(self)
        try:
            if not gobject.signal_lookup("on-change-calendar-window", self):
                gobject.signal_new("on-change-calendar-window",
                                   self,
                                   gobject.SIGNAL_RUN_LAST,
                                   gobject.TYPE_NONE,
                                   (float,))
        except:
            pass

        self.set_modal(True)
        
        if parent_window:
            parent_window.set_transient_for(self)

        hbox = gtk.HBox()
        self.calendar = gtk.Calendar()
        buttonCurrent = gtk.Button()
        buttonDelete  = gtk.Button()

        buttonCurrent.add(gtk.Label("Current"))
        buttonDelete.add(gtk.Label("Delete"))

        hbox.pack_start(buttonCurrent)
        hbox.pack_start(buttonDelete)

        self.vbox.pack_start(self.calendar, False, False)
        self.vbox.pack_start(hbox)

        self.set_decorated(False)
        self.set_position(gtk.WIN_POS_NONE)
        self.set_property("skip-taskbar-hint", True)

        buttonCurrent.connect("pressed", self.do_select_current)
        buttonDelete.connect("pressed", self.do_select_none)
        self.calendar.connect("day-selected-double-click", self.do_select_day)

        self.connect("focus-out-event", self.do_hide_calendar)

        self.value = initial_value

        # if there are a value, select the day
        if self.value:
            year, month, day, hour, minute, second, dow, doy, isdst = time.localtime(self.value)
            self.calendar.select_month(month-1, year)
            self.calendar.select_day(day)

        self.show_all()
        self.action_area.hide()


    def do_hide_calendar(self, calendarwindow, event):
        self.destroy()
        
    def do_select_current(self, button):
        oldvalue = self.value
        self.value = int(time.time()/3600/24) *3600*24
        if oldvalue != self.value:
            self.emit('on-change-calendar-window', (self.value))
        self.destroy()
                
    def do_select_none(self, button):
        oldvalue = self.value
        self.value = 0
        if oldvalue != self.value:
            self.emit("on-change-calendar-window", (self.value))
        self.destroy()
        
    def do_select_day(self, calendar):
        oldvalue = self.value
        value = self.calendar.get_date()
        self.value = time.mktime((value[0], value[1]+1, value[2], 1,0,0, 0,0,0))
        if oldvalue != self.value:
            self.emit("on-change-calendar-window", (self.value))
        self.destroy()

def main():
    w =  CalendarWindow()
    print "el resultado es: ", w.run()

    gtk.main()

if __name__=='__main__':
    main()

