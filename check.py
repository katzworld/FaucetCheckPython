# Description: This script is used to check the faucet status of the user.
import wx
import requests
import datetime
baseUrl = "https://api.tmwstw.io/faucet_state="
faucetType = ["bob", "slag", "grease", "ink"]


class CheckFaucet(wx.Frame):

    def __init__(self, parent, title):
        super(CheckFaucet, self).__init__(parent, title=title, size=(400, 400))

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND)
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.text_ctrl.SetFont(font)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        for faucet in faucetType:
            button = wx.Button(panel, label=faucet)
            button.Bind(wx.EVT_BUTTON, lambda event,
                        faucet=faucet: self.fetch_faucet_data(faucet))
            button_sizer.Add(button, 1, wx.EXPAND)

        sizer.Add(button_sizer, 0, wx.EXPAND)

        panel.SetSizer(sizer)

        self.Show(True)

    def fetch_faucet_data(self, faucet):
        url = baseUrl + faucet
        # print(url)
        response = requests.get(url)
        data = response.json()
        # print(data)
        # data = [[3756, '150'], [4983, '150'], [3531, 0], [5190, 0]]
        fresh_data = []
        for item in data:
            if item[1] != 0:
                fresh_data.append(item[0])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fresh_data.append([timestamp])
        self.text_ctrl.SetValue(str(fresh_data))


app = wx.App()
frame = CheckFaucet(None, "Check Faucet Status")
app.MainLoop()
