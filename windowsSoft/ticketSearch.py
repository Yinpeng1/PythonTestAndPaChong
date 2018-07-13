# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
from train import TranTicket


###########################################################################
## Class TicketFrame
###########################################################################

class TicketFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(1400, 450), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sbSizer7 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"label"), wx.VERTICAL)

        sbSizer7.SetMinSize(wx.Size(1400, 300))
        self.m_panel3 = wx.Panel(sbSizer7.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(1500, -1),
                                 wx.TAB_TRAVERSAL)
        gSizer6 = wx.GridSizer(0, 1, 0, 0)

        gSizer6.SetMinSize(wx.Size(1400, 300))
        self.m_grid14 = wx.grid.Grid(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.Size(1368, 300), 0)

        # Grid
        self.m_grid14.CreateGrid(12, 16)
        self.m_grid14.EnableEditing(True)
        self.m_grid14.EnableGridLines(True)
        self.m_grid14.EnableDragGridSize(False)
        self.m_grid14.SetMargins(0, 0)

        # Columns
        self.m_grid14.EnableDragColMove(False)
        self.m_grid14.EnableDragColSize(True)
        self.m_grid14.SetColLabelSize(30)
        self.m_grid14.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.m_grid14.SetColLabelValue(0, "车次")
        self.m_grid14.SetColLabelValue(1, "出发城市")
        self.m_grid14.SetColLabelValue(2, "目的城市")
        self.m_grid14.SetColLabelValue(3, "历时")
        self.m_grid14.SetColLabelValue(4, "商务/特等")
        self.m_grid14.SetColLabelValue(5, "一等座")
        self.m_grid14.SetColLabelValue(6, "二等座")
        self.m_grid14.SetColLabelValue(7, "高级软卧")
        self.m_grid14.SetColLabelValue(8, "软卧")
        self.m_grid14.SetColLabelValue(9, "动卧")
        self.m_grid14.SetColLabelValue(10, "硬卧")
        self.m_grid14.SetColLabelValue(11, "软座")
        self.m_grid14.SetColLabelValue(12, "硬座")
        self.m_grid14.SetColLabelValue(13, "无座")
        self.m_grid14.SetColLabelValue(14, "其他")
        self.m_grid14.SetColLabelValue(15, "预定")

        # Rows
        self.m_grid14.EnableDragRowSize(True)
        self.m_grid14.SetRowLabelSize(82)
        self.m_grid14.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid14.SetDefaultCellTextColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.m_grid14.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_TOP)
        gSizer6.Add(self.m_grid14, 0, wx.SHAPED, 5)

        self.m_panel3.SetSizer(gSizer6)
        self.m_panel3.Layout()
        sbSizer7.Add(self.m_panel3, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel2 = wx.Panel(sbSizer7.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 20),
                                 wx.TAB_TRAVERSAL)
        fgSizer5 = wx.FlexGridSizer(0, 7, 0, 30)
        fgSizer5.AddGrowableRow(0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        self.m_staticText13 = wx.StaticText(self.m_panel2, wx.ID_ANY, u"出发城市:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)
        self.m_staticText13.SetFont(wx.Font(16, 70, 90, 90, False, wx.EmptyString))

        fgSizer5.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.m_textCtrl11 = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer5.Add(self.m_textCtrl11, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText18 = wx.StaticText(self.m_panel2, wx.ID_ANY, u"到达城市:", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_staticText18.Wrap(-1)
        self.m_staticText18.SetFont(wx.Font(16, 70, 90, 90, False, wx.EmptyString))

        fgSizer5.Add(self.m_staticText18, 0, wx.ALL, 5)

        self.m_textCtrl12 = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer5.Add(self.m_textCtrl12, 0, wx.ALL, 5)

        self.m_staticText19 = wx.StaticText(self.m_panel2, wx.ID_ANY, u"出发日期:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText19.Wrap(-1)
        self.m_staticText19.SetFont(wx.Font(16, 70, 90, 90, False, wx.EmptyString))

        fgSizer5.Add(self.m_staticText19, 0, wx.ALL, 5)

        self.m_textCtrl13 = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer5.Add(self.m_textCtrl13, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(self.m_panel2, wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer5.Add(self.m_button2, 0, wx.ALL, 5)

        self.m_panel2.SetSizer(fgSizer5)
        self.m_panel2.Layout()
        sbSizer7.Add(self.m_panel2, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sbSizer7)
        self.Layout()
        self.m_menubar1 = wx.MenuBar(0)
        self.SetMenuBar(self.m_menubar1)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.search_click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def search_click(self, event):
        event.Skip()


app = wx.App(False)
#根据自己的类名来生成实例
frame = TicketFrame(None)
frame.Show(True)
#start the applications
app.MainLoop()