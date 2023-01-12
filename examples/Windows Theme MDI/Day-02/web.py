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
    icons,
    IconButton,
    border_radius,
)

from MDI import Window,Panel

# Main App Body
class WebAppMDI(UserControl):
    def __init__(self,page: Page,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True
        self.page =page
        #Make Stack layer to full screenn for GestureDetector
        self.desktop = Stack(expand=True)
        self.wm = Stack(expand=True)
        box01 = Window(Row([Container(Text("Content Area",color=colors.BLACK),expand=True)]),self,"Box1",id=1)
        self.wm.controls = [box01]
        self.panel = Panel(app=self)
        self.desktop.controls = [self.panel,self.wm]
        
    def build(self):
        return Container(
            self.desktop,
            expand=True,
            bgcolor=colors.BLUE_100
        )
    
    def __addWindows(self,e):
        count = [i for i in self.wm.controls if i.__class__.__name__ == "Window"]
        count.sort(key=lambda x:x.id)
        id = 1 if len(count) == 0 else count[-1].id + 1
        point = 60 + 20 * id
        box = Window(Row([Container(Text("Content Area",color=colors.BLACK),expand=True)]),self,f"Box{id}",left=point,top=point,id=id)
        self.wm.controls.append(box)
        self.panel.update()
        self.desktop.update()
        
        
    
def main(page: Page):
    page.title = "window manager demo (MDI)"
    page.padding = 0
    app = WebAppMDI(page)
    page.add(app)

if __name__ == '__main__':
    app(target=main,assets_dir="assets")
    