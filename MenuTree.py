#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
from time import sleep
import ttk
import tkFileDialog
import utils1
import xml.etree.ElementTree as ET
import os

DIR = './results/'

class MenuTree:
    def __init__(self):
        self.imagepath = ''
        self.xmlfile = ''
        self.path = ''
        self.package = ''
        self.top = Tk()
        self.top.title('MenuTree')

#Menubar
        self.menubar = Menu(self.top)
        self.menu = Menu(self.menubar, tearoff = 0)
        self.menu.add_command(label = 'Open', command = self.askopenfile)
        self.menubar.add_cascade(label = 'File', menu = self.menu)
        self.top['menu'] = self.menubar

#MainFrame
        self.frame = Frame(self.top)

#LeftFrame:Filter and Treeview
        self.leftFrame = Frame(self.frame)

#FilterFrame
        self.lefttopFrame = Frame(self.leftFrame)
        self.filterFrame = Frame(self.lefttopFrame)
        self.flabel = Label(self.filterFrame, text = 'Filter')
        self.flabel.pack(side = LEFT, padx = 10)
        self.filtervar = StringVar(self.filterFrame)
        self.filtervar.set('All')
        self.filter = OptionMenu(self.filterFrame,
                self.filtervar,
                'All',
                'Manual',
                'Automation'
                )
        self.filter.bind('<Expose>', self.tree_filter)
        self.filter.pack()
        self.filterFrame.pack(side = LEFT, anchor = 'w')

        self.lefttopFrame.pack(anchor = 'w', pady = 5)

#TreeviewFrame
        self.tframe = Frame(self.leftFrame)
        self.sb = Scrollbar(self.tframe,)
        self.sb.pack(side = RIGHT, fill = Y)
        self.show_tree()
        self.leftFrame.pack(side = LEFT, pady = 10, padx = 5)
#LeftFrame end

#RightFrame:Title, Button and Picture
        self.rightFrame = Frame(self.frame)

#TitleFrame
        self.titleFrame = Frame(self.rightFrame)
        self.titlevar = StringVar()
        self.title_label = Label(self.titleFrame, text = 'Title')
        self.title_label.pack(side = LEFT, padx = 15)
        self.title_entry = Entry(self.titleFrame,
                width = 30,
                textvariable = self.titlevar)
        self.titlevar.set('')
        self.title_entry.pack(side = RIGHT)
        self.titleFrame.pack(padx = 10, pady = 5)

#ButtonFrame
        self.buttonFrame = Frame(self.rightFrame)
        self.langLabel = Label(self.buttonFrame, text = 'Language')
        self.langLabel.pack(side = LEFT, padx = 10)
        self.langvar = StringVar(self.buttonFrame)
        self.langvar.set('en_US')
        self.langs = utils1.load_languages("")
        self.lang = OptionMenu(self.buttonFrame,
                self.langvar,
                *self.langs
                )
        self.lang.bind('<Expose>', self.change_lang)
        self.lang.pack(side = LEFT)
        self.capture_button = Button(self.buttonFrame, text = 'Capture')
        self.capture_button.bind('<ButtonRelease>', self.capture)
        self.capture_button.pack(side = LEFT, padx = 10)
        self.save_button = Button(self.buttonFrame, text = 'Save')
        self.save_button.bind('<ButtonRelease>', self.save)
        self.save_button.pack()
        self.buttonFrame.pack(padx = 10, pady = 5)

#PictureFrame
        self.picframe = Frame(self.rightFrame)
        self.canvas = Canvas(self.picframe,
                width = 360,
                height = 640,
                bg = 'white')
        self.show_pic()
        self.canvas.pack()
        self.picframe.pack()

        self.rightFrame.pack(side = RIGHT, padx = 10, pady = 10)
#RightFrame end

        self.frame.pack()
#MainFrame end
        self.top.mainloop()

    def askopenfile(self):
        """
        Openfile Menu
        """

        self.xmlfile =  tkFileDialog.askopenfilename()
        self.path = os.path.split(self.xmlfile)[0]
        self.package = self.path.split('/')[-1]
        self.show_tree()

    def show_tree(self, filter = None):
        """
        Show xml tree in Treeview Frame
        """

        try:
            self.tree.destroy()
        except:
            pass
        self.tree = ttk.Treeview(self.tframe, height = 30,columns=('Type', 'Image'),
                yscrollcommand = self.sb.set)
        self.tree.column("#0",minwidth=300,width=500, stretch=NO)
        self.tree.column("Type", minwidth = 0, width = 0, stretch=NO)
        self.tree.column("Image", minwidth = 0, width = 0, stretch=NO)
        self.create_Tree(filter)
        if self.filtervar.get() != 'All':
            self.tree.tag_configure('filter', foreground = 'red')
        self.tree.bind('<ButtonRelease>', self.select_item)
        self.tree.pack(side = LEFT, fill = BOTH)
        self.sb.config(command = self.tree.yview)
        self.tframe.pack()

    def create_Tree(self, filter = None):
        """
        Read xml file and create root
        """

        try:
            self.dataTree = ET.ElementTree(file = self.xmlfile)
            self.root = self.dataTree.getroot()
            self.parent = self.tree.insert('', END, text = self.root.tag, open=True)
            self.insert(self.root, self.parent, filter)
        except:
            pass

    def insert(self, node, parent, filter = None):
        """
        Insert nodes to the tree
        """

        for child in node:
            if child.attrib['Type'] != filter:
                cid = self.tree.insert(parent,
                        END,
                        text=child.attrib['Title'],
                        values = [child.attrib['Type'],
                            child.attrib['Image'].split('\\')[1]],
                        open=True,
                        tags = 'filter')
                self.insert(child, cid, filter)
            else:
                cid = self.tree.insert(parent,
                        END,
                        text= child.attrib['Title'],
                        values = [child.attrib['Type'],
                            child.attrib['Image'].split('\\')[1]],
                        open=True)
                self.insert(child, cid, filter)

    def select_item(self, event):
        """
        Handle treeview selection event
        """

        curitem = self.tree.item(self.tree.selection())
        self.title = curitem['text']
        if curitem['values']:
            self.type = curitem['values'][0]
            self.imagepath = curitem['values'][1]
        self.titlevar.set(self.title)
        self.show_pic()

    def tree_filter(self, event):
        """
        Handle type filter event
        """

        if self.filtervar.get() == 'All':
            self.show_tree()
        elif self.filtervar.get() == 'Manual':
            self.show_tree('Manual')
        elif self.filtervar.get() == 'Automation':
            self.show_tree('Automation')

    def show_pic(self, path = None):
        """
        Print pics in Picture Frame
        """

        if path:
            imgpath = path
        else:
            imgpath = os.path.join(self.path,'CaptureImages/',self.imagepath+'.png')
        try:
            self.image = Image.open(imgpath)
            size = 360, 640
            self.image.thumbnail(size, Image.ANTIALIAS)
            self.im = ImageTk.PhotoImage(self.image)
            self.img = self.canvas.create_image(180, 320, image = self.im)
        except:
            print "No such pic"

    def change_lang(self, event):
        """
        Handle language change event
        """

        try:
            os.system('adb shell /data/aatpc lang %s' % self.langvar.get())
        except:
            print "Can't change language"

    def capture(self, event):
        """
        Handle capture button event
        """

        self.picname = self.title + '.png'
        os.system('adb shell screencap -p /data/%s' % self.picname)
        sleep(1)
        os.system('adb pull /data/%s tmp/%s' % (self.picname, self.picname))
        self.show_pic('tmp/%s'%self.picname)

    def save(self, event):
        """
        Handle save button event
        """

        des = os.path.join(DIR, self.langvar.get(), self.package)
        if not os.path.exists(des):
            os.makedirs(des)
        print des
        print '%s/%s'%(des, self.picname)
        os.system("mv 'tmp/%s' '%s/%s'" % (self.picname, des, self.picname))

def main():
    t = MenuTree()

if __name__ == "__main__":
    main()
