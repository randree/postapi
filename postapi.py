#!/usr/bin/python3


import gi
from database import Database

from subprocess import PIPE, Popen

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GObject


class PostApiWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="POSTapi")

        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        self.set_icon_name("applications-internet")

        # Start database
        self.db = Database()       

        self.set_default_size(600, 950)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing (6)
        self.grid.set_column_spacing (6)
        self.add(self.grid)

        self.create_textview()
        self.create_toolbar()
        self.create_bottom()

        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)



    def set_url_history (self, entry):
        if entry != "":
            self.history_url.insert(0, entry) if entry not in self.history_url else self.history_url
            self.db.write(entry, 
                self.params1.get_text(), 
                self.params2.get_text(), 
                self.params3.get_text(), 
                self.cookie1.get_text(), 
                self.cookie2.get_text(),
                self.request_method.get_active())

        types = (GObject.TYPE_STRING,)
        store = Gtk.ListStore.new(types)
        for url in self.history_url:
            iter = store.append()
            store.set(iter, 0, url)
        self.url_completion.set_model(store)
        self.url_completion.set_text_column(0)

    def clear_url(self, button):
        self.url.set_text("")


    def create_toolbar(self):
        label = Gtk.Label()
        label.set_label("URL")
        label.set_xalign(1)
        self.grid.attach(label, 0, 0, 1, 1)

        # self.history_url = ["http://192.168.0.22/api/admin/users"]
        self.history_url = self.db.readUrls()

        font = Pango.FontDescription('Monospace 9')

        self.url = Gtk.Entry.new()
        self.url.modify_font(font)
        self.url_completion = Gtk.EntryCompletion.new()
        self.url_completion.connect("match-selected", self.on_change_url) # call if element is selected

        self.url.set_completion(self.url_completion)
        self.url.connect("activate", self.on_click_me_clicked) # call on press enter
        self.set_url_history("")
 
        self.grid.attach(self.url, 1, 0, 4, 1)

        action_box = Gtk.Box(spacing=2) 
        cancel_go = Gtk.Button()       
        cancel_go.set_image(Gtk.Image(stock=Gtk.STOCK_CANCEL))
        cancel_go.connect("clicked", self.clear_url)
        action_box.pack_start(cancel_go, True, True, 0)
        
        button_go = Gtk.Button()
        button_go.set_image(Gtk.Image(stock=Gtk.STOCK_OK))
        button_go.connect("clicked", self.on_click_me_clicked)
        action_box.pack_start(button_go, True, True, 0)

        self.grid.attach(action_box, 5, 0, 1, 1)

        label2 = Gtk.Label()
        label2.set_label("Parameter")
        label2.set_xalign(1)
        self.grid.attach(label2, 0, 1, 1, 1)

        label3 = Gtk.Label()
        label3.set_label("Parameter 2")
        label3.set_xalign(1)
        self.grid.attach(label3, 0, 2, 1, 1)

        label4 = Gtk.Label()
        label4.set_label("Parameter 3")
        label4.set_xalign(1)
        self.grid.attach(label4, 0, 3, 1, 1)

        label5 = Gtk.Label()
        label5.set_label("Cookie Param 1")
        label5.set_xalign(1)
        self.grid.attach(label5, 0, 4, 1, 1)

        label6 = Gtk.Label()
        label6.set_label("Cookie Param 2")
        label6.set_xalign(1)
        self.grid.attach(label6, 0, 5, 1, 1)

        self.params1 = Gtk.Entry()
        self.params1.modify_font(font)
        self.params1.set_text("")
        self.params1.connect("activate", self.on_click_me_clicked)
        self.grid.attach(self.params1, 1, 1, 4, 1)

        self.params2 = Gtk.Entry()
        self.params2.modify_font(font)
        self.params2.set_text("")
        self.params2.connect("activate", self.on_click_me_clicked)
        self.grid.attach(self.params2, 1, 2, 5, 1)

        self.params3 = Gtk.Entry()
        self.params3.modify_font(font)
        self.params3.set_text("")
        self.params3.connect("activate", self.on_click_me_clicked)
        self.grid.attach(self.params3, 1, 3, 5, 1)

        self.cookie1 = Gtk.Entry()
        self.cookie1.modify_font(font)
        self.cookie1.set_text("")
        self.cookie1.connect("activate", self.on_click_me_clicked)
        self.grid.attach(self.cookie1, 1, 4, 5, 1)

        self.cookie2 = Gtk.Entry()
        self.cookie2.modify_font(font)
        self.cookie2.set_text("")
        self.cookie2.connect("activate", self.on_click_me_clicked)
        self.grid.attach(self.cookie2, 1, 5, 5, 1)


        liststore = Gtk.ListStore(str)

        for item in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            liststore.append([item])

        self.request_method = Gtk.ComboBox()
        self.request_method.set_model(liststore)
        self.request_method.set_active(0)
        cellrenderertext = Gtk.CellRendererText()
        self.request_method.pack_start(cellrenderertext, True)
        self.request_method.add_attribute(cellrenderertext, "text", 0)
        # self.request_method.connect("changed", self.on_self.request_method_changed)
        self.grid.attach(self.request_method, 5, 1, 1, 1)

    # Is triggert when a url is selected
    def on_change_url(self, widget, model, iter):
        r = self.db.readParams(model[iter][0])
        self.params1.set_text(r['param1'])
        self.params2.set_text(r['param2'])
        self.params3.set_text(r['param3'])
        self.cookie1.set_text(r['cookie1'])
        self.cookie2.set_text(r['cookie2'])
        self.request_method.set_active(r['method'])

    def on_click_me_clicked(self, button):
        treeiter = self.request_method.get_active_iter()
        model = self.request_method.get_model()

        cookie = ""
        if self.cookie1.get_text() != "" or self.cookie2.get_text() != "" :
            cookie = "'Cookie:" + self.cookie1.get_text()+";" + self.cookie2.get_text()+"'"

        cmd = ("http -v --ignore-stdin --pretty=format " +
         model[treeiter][0] +" " + 
         self.url.get_text() + " " + 
         self.params1.get_text()+" " + 
         self.params2.get_text()+ " "+ 
         self.params3.get_text() +" "+
         cookie +" \n")

        # self.label_bottom_1.set_label(cmd)
        
        # stream = os.popen(cmd)
        # output = stream.read()        

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(cmd+"\n"+stderr.decode("utf-8")+stdout.decode("utf-8"))

        self.textbuffer = self.textview.get_buffer()
        startiter, enditer = self.textbuffer.get_bounds()

        self.set_url_history(self.url.get_text())
        
 
    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 6, 6, 1)

        self.textview = Gtk.TextView()

    
        font = Pango.FontDescription('Monospace 9')
        self.textview.modify_font(font)


        self.textview.set_monospace(True)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("Powered by HTTPie")
        scrolledwindow.add(self.textview)
        
        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD, foreground="blue")

    def create_bottom(self):
        
        font = Pango.FontDescription('Monospace 9')

        self.label_bottom_2 = Gtk.Label()
        self.label_bottom_2.modify_font(font)
        self.label_bottom_2.set_label("Parameter example: test=hallo,\nHeader-parameter example: test:hallo\nCookie-parameter example: test=hallo;foo=bar")
        self.label_bottom_2.set_line_wrap(True)
        self.label_bottom_2.set_xalign(0)

        self.grid.attach(self.label_bottom_2, 0, 7, 6, 1)


win = PostApiWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()