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

#BorderGestureDetector class easy ueuse
class BorderDetector(Container):
    def __init__(self,MouseCursor,event,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = GestureDetector(
            mouse_cursor=MouseCursor,
            drag_interval=10,
            on_horizontal_drag_update=event,
        )

#WinBox Containet
class WinBox(Container):
    def __init__(self,main_content=None,wm=None,title=None,left=20,top=20,*args, **kwargs):
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
        self.main_content = main_content
        #main content use GestureDetector for click winbox put to top layer
        #use on_tap to run __active function
        self.content = GestureDetector(
            content= self.__MainLayer(),
            mouse_cursor=MouseCursor.BASIC,
            drag_interval=5,
            on_tap=self.__active
        )
        
    def __MainLayer(self):
        self.border_left = BorderDetector(
            MouseCursor.RESIZE_LEFT,
            self.__onHorizontalDragLeft,
            left=0,
            width=self.border_line_size,
            height=self.height,
            bgcolor=self.border_line_color 
        )
        self.border_top = BorderDetector(
            MouseCursor.RESIZE_UP,
            self.__onHorizontalDragTop,
            width=self.width,
            height=self.border_line_size,
            bgcolor=self.border_line_color 
        )
        
        self.border_right = BorderDetector(
            MouseCursor.RESIZE_RIGHT,
            self.__onHorizontalDragRight,
            right=0,
            width=self.border_line_size,
            height=self.height,
            bgcolor=self.border_line_color 
        )

        self.border_bottom = BorderDetector(
            MouseCursor.RESIZE_DOWN,
            self.__onHorizontalDragBottom,
            width=self.width,
            bottom=0,
            height=self.border_line_size,
            bgcolor=self.border_line_color 
        )
        
        self.border_topleft = BorderDetector(
            MouseCursor.RESIZE_UP_LEFT,
            self.__onHorizontalDragTopLeft,
            left=0,
            top=0,
            width=3,
            height=3,
        )
        self.border_topright = BorderDetector(
            MouseCursor.RESIZE_UP_RIGHT,
            self.__onHorizontalDragTopRight,
            right=0,
            top=0,
            width=3,
            height=3,
        )
        self.border_bottomright = BorderDetector(
            MouseCursor.RESIZE_DOWN_RIGHT,
            self.__onHorizontalDragBottomRight,
            right=0,
            bottom=0,
            width=3,
            height=3,
        )
        self.border_bottomleft = BorderDetector(
            MouseCursor.RESIZE_DOWN_LEFT,
            self.__onHorizontalDragBottomLeft,
            left=0,
            bottom=0,
            width=3,
            height=3,
        )
        
        return Stack(
            controls=[
                Container(
                    Column(
                        [
                            self.__AppBar(),
                            Container(
                                self.main_content,
                                border_radius=border_radius.only(0,0,5,5),
                                expand=True
                            )                    
                        ],
                        spacing=0
                    ),
                    border_radius=border_radius.all(5),
                    border=border.all(1,colors.BLACK38),
                    bgcolor=colors.WHITE
                ),
                self.border_left,
                self.border_top,
                self.border_right,
                self.border_bottom,
                self.border_topleft,
                self.border_topright,
                self.border_bottomleft,
                self.border_bottomright
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
                    ),
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
###### Here is Mouse Drag and Move and Resice Logic START ######
    def __on_pan_update(self,e: DragUpdateEvent):
        self.top = max(0, self.top + e.delta_y)
        self.left = max(0, self.left + e.delta_x)
        self.update()
        
    def __onHorizontalDragTop(self,e:DragUpdateEvent):
        
        self.height -= e.delta_y
        if self.height < self.defaultHeight:
            self.height = self.defaultHeight
        else:
            self.top = max(0, self.top + e.delta_y)
            self._resizeUpdate()
            self.update()
            
    def __onHorizontalDragBottom(self,e:DragUpdateEvent):
        self.height += e.delta_y
        if self.height < self.defaultHeight:
            self.height = self.defaultHeight
        self._resizeUpdate()
        self.update()
            
    def __onHorizontalDragLeft(self,e:DragUpdateEvent):
        self.width -= e.delta_x
        if (self.width < self.defaultWidth):
            self.width = self.defaultWidth
        else:
            self.left += e.delta_x
            self._resizeUpdate()
            self.update()
            
    def __onHorizontalDragRight(self,e:DragUpdateEvent):
        self.width += e.delta_x
        if (self.width < self.defaultWidth):
            self.width = self.defaultWidth
        self._resizeUpdate()
        self.update()
        
    def __onHorizontalDragTopLeft(self,e:DragUpdateEvent):
            self.__onHorizontalDragLeft(e)
            self.__onHorizontalDragTop(e)
            
    def __onHorizontalDragTopRight(self,e:DragUpdateEvent):
            self.__onHorizontalDragRight(e)
            self.__onHorizontalDragTop(e)
            
    def __onHorizontalDragBottomLeft(self,e:DragUpdateEvent):
            self.__onHorizontalDragLeft(e)
            self.__onHorizontalDragBottom(e)
            
    def __onHorizontalDragBottomRight(self,e:DragUpdateEvent):
            self.__onHorizontalDragRight(e)
            self.__onHorizontalDragBottom(e)
            
    def _resizeUpdate(self):
        self.border_top.width = self.width
        self.border_top.update()
        self.border_bottom.width = self.width
        self.border_bottom.update()
        self.border_left.height = self.height
        self.border_left.update()
        self.border_right.height = self.height
        self.border_right.update()
        
###### Here is Mouse Drag and Move and Resice Logic END ######        
    
    def __close(self,e):
        self.wm.controls = [x for x in self.wm.controls if x.boxuid != self.boxuid] 
        self.wm.update()

    def __active(self,e):
        self.wm.controls = [x for x in self.wm.controls if x.boxuid != self.boxuid] + [self]
        self.wm.update()
        

# Main App Body
class WebAppMDI(UserControl):
    def __init__(self,page: Page,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True
        
        #Make Stack layer to full screenn for GestureDetector
        self.wm = Stack(expand=True)
        
        box01 = WinBox(Row([Container(Text("Content Area",color=colors.BLACK),expand=True)]),self.wm,"Box01")
        self.wm.controls = [box01]
        
    def build(self):
        return Container(Column([self.wm,self.__addboxBTN()],spacing=0),expand=True,bgcolor=colors.BLUE_100)
    
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
            bgcolor=colors.BLACK45,
            padding=Padding(10,5,10,3)
        )
    def __addBox(self,e):
        count = len([i for i in self.wm.controls if i.__class__.__name__ == "WinBox"])
        id = count + 1 
        point = 20 * id
        box = WinBox(Row([Container(Text("Content Area",color=colors.BLACK),expand=True)]),self.wm,f"Box{id}",left=point,top=point)
        self.wm.controls.append(box)
        self.wm.update()
    
def main(page: Page):
    page.title = "window manager demo (MDI)"
    page.padding = 0
    app = WebAppMDI(page)
    page.add(app)

if __name__ == '__main__':
    app(target=main,assets_dir="assets")
    