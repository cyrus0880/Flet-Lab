from flet import (
    app,
    Page,
    Column,
    colors,
    Row,
    Container,
    UserControl,
    Stack,
    Padding,
    Text,
    GestureDetector,
    MouseCursor,
    Icon,
    icons,
    IconButton,
    FontWeight,
    border_radius,
    border,
    DragUpdateEvent
)

import uuid


#WinBox Containet
class WinBox(Container):
    def __init__(self,wm,title,left=20,top=20,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # Container Prop
        self.boxuid = str(uuid.uuid4()) # WinBox uid for active or wm controller
        self.defaultWidth = 400
        self.defaultHeight = 250
        self.border_line_size = 2
        self.border_line_color = None  
        self.border_radius = 5
        self.appbar_color = colors.BLACK12
        self.width = self.defaultWidth
        self.height = self.defaultHeight
        uid = self.boxuid.split("-")[-1]
        self.title = Row([
            Icon(icons.APPS_OUTLINED,color=colors.BLACK,scale=0.8),
            Text(title,color=colors.BLACK,scale=0.8,weight=FontWeight.W_900),
            Text(f"uid : {uid}",color=colors.BLACK,scale=0.8,weight=FontWeight.W_900)
        ])
        self.left=left
        self.top=top
        self.wm = wm
        
        #main content use GestureDetector for click winbox put to top layer
        #use on_tap to run __active function
        self.content = GestureDetector(
            content= self.__MainLayer(),
            mouse_cursor=MouseCursor.BASIC,
            drag_interval=5,
            on_tap=self.__active
        )
        
        
    def __MainLayer(self):
        return Stack(
            controls=[
                Container(
                    Column(
                        [
                            self.__AppBar(),
                            Container(
                                Row(expand=True),
                                expand=True,
                                border_radius=border_radius.only(0,0,5,5)
                            )                    
                        ],
                        spacing=0
                    ),
                    border_radius=border_radius.all(5),
                    border=border.all(1,colors.BLACK38),
                    bgcolor=colors.WHITE
                ),
            ]
        )
    def __AppBar(self):
        layout = Container(
            content=Row(
                [
                    Container(self.title,expand=True),
                    Container(
                        Row(
                            [
                                Icon(icons.REMOVE,color=colors.BLACK54,scale=0.6),
                                Icon(icons.FULLSCREEN,color=colors.BLACK54,scale=0.6),
                               Container(Icon(icons.CLOSE,color=colors.BLACK54,scale=0.6),on_click=self.__close),
                            ],
                            spacing=0
                        ),
                    )
                ]
            ),
            padding=Padding(6,2,6,2),
            border_radius=border_radius.only(5,5,0,0),
            border=border.only(bottom=border.BorderSide(1,colors.BLACK38)),
            bgcolor=self.appbar_color
        )
        return GestureDetector(
            layout,
            mouse_cursor=MouseCursor.BASIC,
            drag_interval=1,
            on_pan_update=self.__on_pan_update,
        )
        
    def __on_pan_update(self,e: DragUpdateEvent):
        self.top = max(0, self.top + e.delta_y)
        self.left = max(0, self.left + e.delta_x)
        self.update()

    def __close(self,e):
        self.wm.controls = [x for x in self.wm.controls if x.boxuid != self.boxuid] 
        self.wm.update()

    def __active(self,e):
        self.wm.controls = [x for x in self.wm.controls if x.boxuid != self.boxuid] + [self]
        self.wm.update()

class WebAppMDI(UserControl):
    def __init__(self,page: Page,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True
        
        
        
        #Make Stack layer to full screenn for GestureDetector
        self.wm = Stack(expand=True)
        
        box01 = WinBox(self.wm,"Box01")
        self.wm.controls = [box01]
        
    def build(self):
        return Container(Column([self.wm,self.__addboxBTN()]),expand=True,bgcolor=colors.BLUE_100)
    
    def __addboxBTN(self):
        return Container(
            Row(
                [
                    Container(
                        IconButton(icons.ADD,icon_color=colors.WHITE,on_click=self.__addBox),
                        border_radius=border_radius.all(20),
                        bgcolor=colors.BLACK45,
                    )
                ],
            ),
            padding=Padding(10,10,10,10)
        )
    def __addBox(self,e):
        count = len([i for i in self.wm.controls if i.__class__.__name__ == "WinBox"])
        id = count + 1 
        point = 20 * id
        box = WinBox(self.wm,f"Box{id}",left=point,top=point)
        self.wm.controls.append(box)
        self.wm.update()
    
def main(page: Page):
    page.title = "window manager demo (MDI)"
    page.padding = 0
    app = WebAppMDI(page)
    page.add(app)

if __name__ == '__main__':
    app(target=main,assets_dir="assets")
    