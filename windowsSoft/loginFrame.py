import wx
import wx.lib.sized_controls as wxsc

# ~ #-------------------------------------------------
# ~ #set value for widgets( StaticText and TextCtrl) height
wh = 30
# ~ #set value for max width times
mwt = 8
# ~ #set value for  wh times
wht = 3


# ~ #-------------------------------------------------
class InputDialog(wxsc.SizedDialog):

    def __init__(self, title='Setting values:', values={'int': 1, 'String': 'This is String', 'float': 3.5}):
        '''
        #~ using it as follow:
        #~ dialog = InputDialog(title='Setting values:',values={'int':1,'String':'This is String','float':3.5})
        #~ just for test:
        #~ dialog = InputDialog()
        '''
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wxsc.SizedDialog.__init__(self, parent=None, id=-1, title=title, style=style)

        self.originvalues = values.copy()
        self.modifiedvalues = values.copy()
        self.pane = self.GetContentsPane()
        self.pane.SetSizerType("form")

        maxlen1 = mwt * max([len(str(key)) for key in values])
        if maxlen1 < wh * wht:
            maxlen1 = wh * wht

        maxlen2 = mwt * max([len(str(values[key])) for key in values])
        if maxlen2 < wh * wht:
            maxlen2 = wh * wht

        for key in self.modifiedvalues:
            keyStr = str(key)
            label = keyStr + ' :'
            StaticText = wx.StaticText(parent=self.pane, id=-1, label=label, style=wx.ALIGN_RIGHT)
            StaticText.SetInitialSize((maxlen1, wh))
            value = str(self.modifiedvalues[key])
            TextCtrl = wx.TextCtrl(parent=self.pane, id=-1, value=value)
            TextCtrl.SetInitialSize((maxlen2, wh))
            TextCtrl.SetSizerProps(expand=True)
            # ~set a name for TextCtrl,so later we can use wx.FindWindowByName()
            TextCtrl.Name = 'TC_' + str(keyStr)
            # StaticText.Name='ST_'+str(keyStr)

        # ~ # add dialog buttons
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))

        self.Fit()
        self.Center()

    def GetOriginValue(self):
        '''
        #~ if the user select wx.ID_CANCEL,then return originvalues
        '''
        return self.originvalues

    def GetValue(self):
        '''
        #~ if the user select wx.ID_OK,then return self.modifiedvalues
        '''
        for key in self.modifiedvalues:
            keyStr = str(key)
            TextCtrlName = 'TC_' + str(keyStr)
            TextCtrl = self.FindWindowByName(TextCtrlName)
            ovk = self.modifiedvalues[key]
            if (type(ovk) == int):
                self.modifiedvalues[key] = int(TextCtrl.GetValue().strip())
            elif (type(ovk) == float):
                self.modifiedvalues[key] = float(TextCtrl.GetValue().strip())
            else:
                self.modifiedvalues[key] = str(TextCtrl.GetValue())

        return self.modifiedvalues


# ~ #-------------------------------------------------
def InputBox(title='Setting values', values={'int': 1, 'String': 'This is String', 'float': 3.5}):
    '''
    #~ >>>values={'int':1,'String':'This is String','float':3.5}
    #~ >>>title='Setting values:'
    #~ >>>rvalues=InputBox(title,values)
    #~ >>>print(rvalues):
    '''
    app = wx.PySimpleApp()
    dialog = InputDialog(title=title, values=values)
    if dialog.ShowModal() == wx.ID_OK:
        values = dialog.GetValue()
    else:
        values = dialog.GetOriginValue()

    dialog.Destroy()
    app.MainLoop()
    return values


##~ #测试InputBox
# if __name__ == '__main__':
# values={'int':1,'String':'This is String','float':3.5}
# title='Setting values'
# rvalues=InputBox(title,values=values)
# print(rvalues)

##~ #-------------------------------------------------
class InputPanel(wx.Panel):
    def __init__(self, parent, label='Setting values:', values={'int': 1, 'String': 'This is String', 'float': 3.5}):
        '''
        #~ >>>ipl = InputPanel(parent,label='Setting values:',values={'int':1,'String':'This is String','float':3.5})
         #~>>> rvalues=ipl.GetValue(self)
        '''
        wx.Panel.__init__(self, parent=parent, id=-1)

        self.modifiedvalues = values.copy()

        box = wx.StaticBox(self, -1, label=label)
        sbsizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        gridsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)

        maxlen1 = mwt * max([len(str(key)) for key in values])
        if maxlen1 < wh * wht:
            maxlen1 = wh * 3

        maxlen2 = mwt * max([len(str(values[key])) for key in values])
        if maxlen2 < wh * wht:
            maxlen2 = wh * wht

        for key in self.modifiedvalues:
            keyStr = str(key)
            label = keyStr + ' :'
            StaticText = wx.StaticText(parent=self, id=-1, label=label, style=wx.ALIGN_RIGHT)
            StaticText.SetInitialSize((maxlen1, wh))
            gridsizer.Add(StaticText, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 3)
            value = str(self.modifiedvalues[key])
            TextCtrl = wx.TextCtrl(parent=self, id=-1, value=value)
            TextCtrl.SetInitialSize((maxlen2, wh))
            gridsizer.Add(TextCtrl, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 3)

            # ~set a name for TextCtrl,so later we can use wx.FindWindowByName()
            TextCtrl.Name = 'TC_' + str(keyStr)

        sbsizer.Add(gridsizer, 1, wx.EXPAND)
        gridsizer.Layout()
        PanelSizer = wx.BoxSizer(wx.VERTICAL)
        PanelSizer.Add(sbsizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(PanelSizer)
        PanelSizer.Layout()
        PanelSizer.Fit(self)

    def GetValue(self):
        '''
        #~ return self.modifiedvalues
        '''
        for key in self.modifiedvalues:
            keyStr = str(key)
            TextCtrlName = 'TC_' + str(keyStr)
            TextCtrl = self.FindWindowByName(TextCtrlName)
            ovk = self.modifiedvalues[key]
            if (type(ovk) == int):
                self.modifiedvalues[key] = int(TextCtrl.GetValue().strip())
            elif (type(ovk) == float):
                self.modifiedvalues[key] = float(TextCtrl.GetValue().strip())
            else:
                self.modifiedvalues[key] = str(TextCtrl.GetValue())

        return self.modifiedvalues

    ##~ #-------------------------------------------------


class InputFrame(wx.Frame):
    def __init__(self, title='InputFrame:', label='Setting values:',
                 values={'int': 1, 'String': 'This is String', 'float': 3.5}, size=(400, 200)):
        '''
        #~ >>>IFrame = InputFrame(title='InputFrame:',label='Setting values:',values={'int':1,'String':'This is String','float':3.5},size=(400,200)):
         #~>>> rvalues=IFrame.GetValue()
        '''
        wx.Frame.__init__(self, parent=None, title=title, size=size)
        self.modifiedvalues = values.copy()
        self.IPL = InputPanel(self, label=label, values=values)
        # ~ #创建FlexGridSizer
        self.FlexGridSizer = wx.FlexGridSizer(rows=9, cols=1, vgap=5, hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)

        self.RightPanel = wx.Panel(self, -1)

        # ~ #测试按钮1
        self.Button1 = wx.Button(self.RightPanel, -1, "TestButton", size=(100, 40), pos=(10, 10))
        self.Button1.Bind(wx.EVT_BUTTON, self.GetValue)
        # ~ #加入Sizer中
        self.FlexGridSizer.Add(self.Button1, proportion=0, border=5, flag=wx.ALL | wx.EXPAND)
        self.RightPanel.SetSizer(self.FlexGridSizer)
        self.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BoxSizer.Add(self.IPL, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)
        self.BoxSizer.Add(self.RightPanel, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.BoxSizer)
        self.Center(wx.BOTH)

    # ~ #按钮事件,用于测试
    def GetValue(self, event):
        self.modifiedvalues = self.IPL.GetValue()
        # ~ print(self.modifiedvalues)
        return self.modifiedvalues


# ~ #主程序测试
def TestInputFrame():
    app = wx.PySimpleApp()
    title = 'InputFrame:'
    label = 'Setting values:'
    values = {'int': 234, 'String': 'This is String', 'float': 3.5}
    frame = InputFrame(title, label, values)
    frame.Show()
    app.MainLoop()
    return


if __name__ == '__main__':
    app = wx.App()
    title = 'InputFrame:'
    label = 'Setting values:'
    values = {'int': 234, 'String': 'This is String', 'float': 3.5}
    frame = InputFrame(title, label, values)
    frame.Show()
    app.MainLoop()
