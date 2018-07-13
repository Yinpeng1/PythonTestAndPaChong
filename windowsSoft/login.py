# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from windowsSoft.dbConnection import checkUser

###########################################################################
## Class BaseFrame
###########################################################################

class BaseFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"抢票系统登陆"), wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"用户名:", wx.Point(-1, -1),
                                           wx.Size(100, 25), 0)
        self.m_staticText4.Wrap(-1)
        self.m_staticText4.SetFont(wx.Font(20, 70, 90, 90, False, wx.EmptyString))

        sbSizer1.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.Point(101, -1),
                                       wx.Size(500, 30), 0)
        sbSizer1.Add(self.m_textCtrl3, 0, wx.ALL, 5)

        self.m_staticText8 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"密码:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        self.m_staticText8.SetFont(wx.Font(20, 70, 90, 90, False, wx.EmptyString))

        sbSizer1.Add(self.m_staticText8, 0, wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.Size(500, 30), 0)
        sbSizer1.Add(self.m_textCtrl4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        m_sdbSizer2 = wx.StdDialogButtonSizer()
        self.m_sdbSizer2OK = wx.Button(sbSizer1.GetStaticBox(), wx.ID_OK)
        m_sdbSizer2.AddButton(self.m_sdbSizer2OK)
        self.m_sdbSizer2Cancel = wx.Button(sbSizer1.GetStaticBox(), wx.ID_CANCEL)
        m_sdbSizer2.AddButton(self.m_sdbSizer2Cancel)
        m_sdbSizer2.Realize();

        sbSizer1.Add(m_sdbSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(sbSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_sdbSizer2Cancel.Bind(wx.EVT_BUTTON, self.cancel_button_click)
        self.m_sdbSizer2OK.Bind(wx.EVT_BUTTON, self.ok_button_click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def cancel_button_click(self, event):
        self.Close()

    def ok_button_click(self, event):
        # event.Skip()
        username = self.m_textCtrl3.GetValue()
        password = self.m_textCtrl4.GetValue()
        print(username + "---" + password)
        result = checkUser(username, password)
        if result == 1:
            print("good")
        else:
            print("bad")

app = wx.App(False)
#根据自己的类名来生成实例
frame = BaseFrame(None)
frame.Show(True)
#start the applications
app.MainLoop()

