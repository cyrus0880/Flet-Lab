
from flet import (
    Page,
    Column,
    colors,
    Row,
    Container,
    Stack,
    Padding,
    Text,
    GestureDetector,
    MouseCursor,
    Icon,
    icons,
    FontWeight,
    border_radius,
    border,
    DragUpdateEvent,
    MainAxisAlignment,
    IconButton,
    ButtonStyle
)

# thking howto add relocation panel to other edge position  
class Position:
    left = {'left':0,'object':Column()}
    top = {'top':0,'object':Row()}
    right = {'right':0,'object':Column()}
    bottom = {'bottom':0,'object':Row()}


# Trays Widget docking windows btn in here
class Trays(Row):
    def __init__(self,app,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.controls = []
    
    def getWM(self):
        wms = []
        for win in self.app.wm.controls:
            container =TrayIcon(win)
            wms.append(container)
        wms.sort(key=lambda x:x.id)
        self.controls = wms
        
# Windows Tray Btn widget
class TrayIcon(Container):
    def __init__(self,winbox,*args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.winbox = winbox
        self.id = winbox.id
        self.boxuid = self. winbox.boxuid
        self.title = self.winbox.title.controls[1].value
        self.icon = self.winbox.icon
        self.height= 25
        self.width= 25
        self.padding = Padding(0,0,0,2)
        if winbox.active:
            self.border = border.only(bottom=border.BorderSide(2,color=colors.GREEN))
        elif winbox.visible:
            self.border = border.only(bottom=border.BorderSide(2,color=colors.RED))
            
        self.content = self.MainIcon()
        self.update = self.__update
        
    def MainIcon(self):
        return IconButton(
            self.icon,
            icon_size=23,
            tooltip=self.title,
            scale=self.scale,
            style=ButtonStyle(padding=Padding(0,0,0,0)),
            on_click=self.winbox._Window__show
        )
    
    def __update(self,e):
        print("update")

        
    
# PanelBar Widget MainUI can put other widget in here (eg:Tray,clock,logout btn,start menu btn)
class Panel(Container):
    def __init__(self,app=None,widgets=[],position=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.height = 35
        self.bgcolor = colors.BLACK45
        self.padding = Padding(10,5,10,5)
        self.ListWM = Trays(self.app)
        self.update = self.__update
        self.update()
        self.widgets = widgets
        self.content = self.PanelLayout()
        
        
        
    def PanelLayout(self):
        LogoutBtn = Container(
            IconButton(icons.EXIT_TO_APP,icon_color=colors.WHITE,icon_size=15,style=ButtonStyle(padding=Padding(0,0,0,0)),on_click=self.__logout),
            height= 25,
            width= 25,
            border_radius=border_radius.all(20),
            bgcolor=colors.BLACK45,
        )
        AddBTN = Container(
            IconButton(icons.ADD,icon_color=colors.WHITE,icon_size=15,style=ButtonStyle(padding=Padding(0,0,0,0)),on_click=self.__addWindows),
            height= 25,
            width= 25,
            border_radius=border_radius.all(20),
            bgcolor=colors.BLACK45,
        )
        widgets = [LogoutBtn,AddBTN] if len(self.widgets) == 0 else [AddBTN,self.widgets]
        return Row(widgets)
    def __update(self):
        self.ListWM.getWM()
                                
    def __showWin(self,win):
        win._Window__show(None)
    def __addWindows(self,e):
        self.app._WebAppMDI__addWindows(e)
    def __logout(self,e):
        token = self.app.page.client_storage.get("token")
        if token :
            self.app.page.client_storage.remove("token")
            self.app.CheckLogin()
    