import wx
import wx.lib.scrolledpanel as scrolled
import pyglet
import os
from wx.lib.filebrowsebutton import FileBrowseButton

class MPlayerFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MPlayerFrame, self).__init__(parent, title=title, size=(600, 400))
        icon = wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO)  # Replace icon.ico with your icon file
        self.SetIcon(icon)
        self.playlist = []
        self.current_song = None
        self.player = None
        self.volume = 1.0
        self.CreateUI()
        self.Centre()
        self.Show()

    def CreateUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_browse_button = FileBrowseButton(panel,labelText="Выбрать файлы", fileMask="*.mp3;*.wav;*.ogg",
                                                   size=(300,-1),changeCallback=self.onBrowse)
        hbox1.Add(self.file_browse_button, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.ALL, 5)

        self.playlist_panel = scrolled.ScrolledPanel(panel, -1, style=wx.SIMPLE_BORDER)
        self.playlist_sizer = wx.BoxSizer(wx.VERTICAL)
        self.playlist_panel.SetSizer(self.playlist_sizer)
        self.playlist_panel.SetupScrolling()
        vbox.Add(self.playlist_panel, 1, wx.EXPAND | wx.ALL, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.play_button = wx.Button(panel, label="Воспроизвести")
        self.play_button.Bind(wx.EVT_BUTTON, self.onPlay)
        hbox2.Add(self.play_button, 0, wx.ALL, 5)

        self.stop_button = wx.Button(panel, label="Остановить")
        self.stop_button.Bind(wx.EVT_BUTTON, self.onStop)
        hbox2.Add(self.stop_button, 0, wx.ALL, 5)

        volume_text = wx.StaticText(panel, label="Громкость:")
        hbox2.Add(volume_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.volume_slider = wx.Slider(panel, value=100, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)
        self.volume_slider.Bind(wx.EVT_SCROLL, self.onVolumeChange)
        hbox2.Add(self.volume_slider, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox2, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)

    def onBrowse(self, event):
        filepath = event.GetString()
        if filepath and filepath not in self.playlist:
            self.playlist.append(filepath)
            self.updatePlaylist()

    def updatePlaylist(self):
        self.playlist_sizer.Clear(True)
        for song in self.playlist:
            text = wx.StaticText(self.playlist_panel, label=song)
            self.playlist_sizer.Add(text, 0, wx.ALL, 5)
        self.playlist_panel.Layout()
        self.playlist_panel.SetupScrolling()
        self.playlist_panel.Refresh()

    def onPlay(self, event):
        if self.playlist:
            filepath = self.playlist[0]
            try:
                if self.player:
                    self.player.pause()
                self.player = pyglet.media.Player()
                self.current_song = pyglet.media.load(filepath)
                self.player.queue(self.current_song)
                self.player.play()
                self.volume_slider.SetValue(int(self.volume * 100))
            except Exception as e:
                wx.MessageBox(f"Ошибка воспроизведения: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def onStop(self, event):
        if self.player:
            self.player.pause()
            self.player.delete()
            self.player = None
            self.current_song = None

    def onVolumeChange(self, event):
        self.volume = self.volume_slider.GetValue() / 100
        if self.player and self.player.playing:
            self.player.volume = self.volume

if __name__ == "__main__":
    app = wx.App()
    frame = MPlayerFrame(None, "M-Player")
    app.MainLoop()