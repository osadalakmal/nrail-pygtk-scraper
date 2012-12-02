#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import httplib
from HTMLParser import HTMLParser
from comboboxcalendar import ComboBoxCalendar
import inspect
import time
import pdb

STATION_CODE_MAP = { "Stevenage" : "SVG", "Grantham":"GRA", "Peterborough":"PBO" }

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

class Journey:

    def __init__(self):
        self.frm = ""
        self.to = ""
        self.stime = ""
        self.etime = ""
        self.price = ""

    def _init__(self,frm,to,etime,stime):
        if (frm == "" or to == "" or ((etime != "") != (stime != ""))):
            raise ValueError("Incorrect arguments passed in")  
        self.frm = frsm
        self.to = to
        self.stime = stime
        self.etime = etime
        self.price = ""

    def set_from(self,frm):
        self.frm = frm

    def set_to(self,to):
        self.to = to

    def set_stime(self,stime):
        self.stime = stime

    def set_etime(self,etime):
        self.etime = etime

    def set_price(self,price):
        self.price = price

    def __str__(self):
        return "from:" + str(self.frm) + " to:" + str(self.to) + \
               " stime:" + str(self.stime) + " etime:" + str(self.etime) + \
               " price:" + str(self.price)

    def as_tuple(self):
        print (str(self.frm),str(self.to),str(self.stime),str(self.etime),str(self.price))
        return (str(self.frm),str(self.to),str(self.stime),str(self.etime),str(self.price))

class MyHTMLParser(HTMLParser):
    
    def __init__(self):
        self.mode = 0
        self.prop = Journey.set_from
        self.journeys = []
        self.curjourney = Journey()
        
        HTMLParser.__init__(self) 

    def handle_starttag(self, tag, attrs):
        if (self.mode == 2 and tag == 'tbody'):
            self.mode = 1
        for attr in attrs:
            if (attr[0] == 'id' and attr[1] == 'oft'):
                self.mode = 2;
            if (self.mode ==1 and tag == 'tr' and self.curjourney.frm != ""):
                self.journeys.append(self.curjourney)
                self.curjourney = Journey()
            if (self.mode == 1 and attr[0] == 'class' and attr[1] == 'from'):
                self.prop = Journey.set_from
            if (self.mode == 1 and attr[0] == 'class' and attr[1] == 'to'):
                self.prop = Journey.set_to
            if (self.mode == 1 and attr[0] == 'class' and attr[1] == 'dep'):
                self.prop = Journey.set_stime
            if (self.mode == 1 and attr[0] == 'class' and attr[1] == 'arr'):
                self.prop = Journey.set_etime
            if (self.mode == 1 and attr[0] == 'id' and attr[1][0:4] == 'fare'):
                self.mode = 4
                self.prop = Journey.set_price
            if (self.mode == 1 and tag == 'abbr'):
                self.mode == 3
    def handle_endtag(self, tag):
        if (tag == 'table' and self.mode == 1):
            self.mode = 0;
        elif (self.mode == 3 and tag == 'abbr'):
            self.mode = 1
    def handle_data(self, data):
        if (self.prop == Journey.set_price and self.mode == 4):
            self.mode = 1
            return
        if (self.mode == 1 and self.prop != None):
            if (self.prop == Journey.set_from or self.prop == Journey.set_to):
                nData = data[0:data.find('[')-1]
                self.prop(self.curjourney,nData.strip())
            else:
                self.prop(self.curjourney,data)
            self.prop = None
    def handle_comment(self, data):
        pass 
    def handle_entityref(self, name):
        pass 
    def handle_charref(self, name):
        pass 
    def handle_decl(self, data):
        pass
    def getJourneys(self):
        return self.journeys

def buildModel(button,app):
    frm = STATION_CODE_MAP[app.fromEntry.get_active_text()]
    to = STATION_CODE_MAP[app.toEntry.get_active_text()]
    print frm
    print to
    dateValue = time.strftime("%d%m%y",time.localtime(app.date.value))
    stime = ""
    etime = ""
    journeys = []
    if (app.eTimeCB.get_active()):
        etime = str(app.timHour.get_value_as_int()).zfill(2) + \
                str(app.timMin.get_value_as_int()).zfill(2)
        try:
            Journey(frm,to,etime,stime)
            journeys = getTrains(frm,to,dateValue,etime,"arr")
        except:
            return
    else:
        stime = str(app.timHour.get_value_as_int()).zfill(2) + \
                str(app.timMin.get_value_as_int()).zfill(2)
        try:
            Journey(frm,to,etime,stime)
            journeys = getTrains(frm,to,dateValue,stime,"dep")
        except:
            return
    app.liststore.clear()
    for journey in journeys:
        app.liststore.append(journey.as_tuple())

def setBestPrice(model,path,iterator,app):
    bestPrice = 10000.00
    bestRow = -1
    for idx,row in enumerate(model):
        if row[4] != None and bestPrice > float(row[4]):
            bestPrice = float(row[4])
            bestRow = idx
            app.listview.get_selection().select_path((idx,))
            app.priceValue.set_text(str(bestPrice))

def getTrains(fromStation,toStation,date,time,timeType):
    conn = httplib.HTTPConnection('ojp.nationalrail.co.uk')
    conn.request('GET','/service/timesandfares/' + fromStation + "/" + \
                 toStation + '/' + date + '/' + time + '/' + timeType)
    resp = conn.getresponse()
    if (resp.status != 200 and resp.reason != 'OK'):
        print "Could not complete http request"
        print "status:" + str(resp.status) + " reason:" + str(resp.reason)
        exit()
    data = resp.read()
    parser = MyHTMLParser()
    parser.feed(data)
    return parser.getJourneys()

class MainApp:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Easy Rail Ticket Example")
        #self.window.set_size_request(200, 200)
        self.window.connect("delete_event", self.delete_event)
        self.table = gtk.Table(16,9)
        self.CreateInputs()
        self.CreateList()
        self.window.add(self.table)
        self.window.show_all()

    def CreateInputs(self):
        self.fromLabel = gtk.Label("From")
        self.table.attach(self.fromLabel,1,2,1,2,xpadding=5)
        self.fromEntry = gtk.combo_box_new_text()
        self.fromEntry.append_text('Stevenage')
        self.fromEntry.append_text('Grantham')
        self.fromEntry.append_text('Peterborough')
        self.table.attach(self.fromEntry,2,3,1,2,xpadding=10,ypadding=10)
        self.toLabel = gtk.Label("To")
        self.table.attach(self.toLabel,3,4,1,2,xpadding=5)
        self.toEntry = gtk.combo_box_new_text()
        self.toEntry.append_text('Stevenage')
        self.toEntry.append_text('Grantham')
        self.toEntry.append_text('Peterborough')
        self.table.attach(self.toEntry,4,5,1,2,xpadding=10,ypadding=10)
        self.date = ComboBoxCalendar("Journey Date",parent_window=self.window)
        self.table.attach(self.date,5,6,1,2)
        
        self.timeFrame = gtk.Frame("Times")
        self.timeCBFrameBox = gtk.HBox()
        self.timeCBFrameBox.pack_start(self.CreateTimeCB(),True,True,8)
        self.timeCBFrameBox.pack_start(gtk.Label("Hour"),True,True,5)
        self.hourAdj = gtk.Adjustment(value=07, lower=00, upper=23, step_incr=1, page_incr=5, page_size=0)
        self.timHour = gtk.SpinButton(self.hourAdj,1,0)
        self.timeCBFrameBox.pack_start(self.timHour,True,True,8)
        self.timeCBFrameBox.pack_start(gtk.Label(" Min"),True,True,5)
        self.minAdj = gtk.Adjustment(value=30, lower=00, upper=59, step_incr=1, page_incr=5, page_size=0)
        self.timMin = gtk.SpinButton(self.minAdj,1,0)
        self.timeCBFrameBox.pack_start(self.timMin,True,True,8)
        self.timeFrame.add(self.timeCBFrameBox)
        self.table.attach(self.timeFrame,1,5,2,3,xpadding=5,ypadding=5)

        self.priceLabel = gtk.Label("Best Price")
        self.table.attach(self.priceLabel,5,6,2,3, xpadding=5)
        self.priceValue = gtk.Label("0.00")
        self.table.attach(self.priceValue,6,7,2,3, xpadding=5)
        self.getButton = gtk.Button("Get Prices")
        self.table.attach(self.getButton,7,8,1,2,True,True,xpadding=5)
        self.getButton.connect("clicked",buildModel,self)

    def CreateTimeCB(self):
        self.timeCBBox = gtk.VBox(False, 3)
        self.sTimeCB = gtk.RadioButton(None, 'Arrive')
        self.eTimeCB = gtk.RadioButton(self.sTimeCB,'Depart')
        self.timeCBBox.add(self.sTimeCB)
        self.timeCBBox.add(self.eTimeCB)
        return self.timeCBBox


    def CreateList(self):
        self.liststore = gtk.ListStore(str,str,str,str,str)
        self.liststore.connect("row-changed",setBestPrice,self)

        # create the TreeView using treestore
        self.listview = gtk.TreeView(self.liststore)
        
        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # create the TreeViewColumn to display the data
        self.lvcolumn1 = gtk.TreeViewColumn('From', self.cell, text = 0)
        self.lvcolumn2 = gtk.TreeViewColumn('To', self.cell, text = 1)
        self.lvcolumn3 = gtk.TreeViewColumn('Dep Time', self.cell, text = 2)
        self.lvcolumn4 = gtk.TreeViewColumn('Arr Time', self.cell, text = 3)
        self.lvcolumn5 = gtk.TreeViewColumn('Price', self.cell, text = 4)

        # add tvcolumn to treeview
        self.listview.append_column(self.lvcolumn1)
        self.listview.append_column(self.lvcolumn2)
        self.listview.append_column(self.lvcolumn3)
        self.listview.append_column(self.lvcolumn4)
        self.listview.append_column(self.lvcolumn5)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.lvcolumn1.add_attribute(self.cell, 'text', 0)
        self.listview.set_search_column(0)
        self.lvcolumn1.set_sort_column_id(0)
        self.listview.set_reorderable(True)
        self.table.attach(self.listview,1,12,6,12,ypadding=5)

def main():
    gtk.main()

if __name__ == "__main__":
    tvexample = MainApp()
    main()
