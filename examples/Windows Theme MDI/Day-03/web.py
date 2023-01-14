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
    ProgressRing,
    alignment
)
import time
from MDI import Window,Panel
from Auth.htpassAuth import Auth
from Login import Login


class Session():
    def __init__(self):
        self.local = {}
        self.auth = {}


# Main App Body
class WebAppMDI(UserControl):
    def __init__(self,page: Page,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = Session()
        self.expand = True
        self.page = page
        #Make Stack layer to full screenn for GestureDetector
        self.desktop = Stack(expand=True)
        self.wm = Stack(expand=True)
        box01 = Window(Row([Container(Text("Content Area",color=colors.BLACK),expand=True)]),self,"Box1",id=1)
        self.wm.controls = [box01]
        self.panel = Panel(app=self)
        self.desktop.controls = [self.panel,self.wm]
        self.MainPage = Container(self.desktop,bgcolor=colors.BLUE_100,expand=True)
        
    def build(self):
        self.session.local['page'] = Row(expand=True,alignment='center')
        self.session.local['page'].controls.append(ProgressRing(scale=1,color=colors.BLACK45))
        return Container(
            Column([
                self.session.local['page'],
            ]),
            #bgcolor=colors.BLUE_100
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
        
    def run(self):
        self.CheckLogin()  
           
    def CheckLogin(self):
        token = self.page.client_storage.get("token")
        auth = Auth()
        self.session.local['page'].controls[0] = Login(self)
        
        if auth.Chk_Token(token):
            self.session.local['page'].controls[0] = self.MainPage
        else:
            self.session.local['page'].controls[0] = Login(self)
        self.update()        
    
def main(page: Page):
    page.title = "window manager demo (MDI)"
    page.padding = 0
    
    app = WebAppMDI(page)
    page.add(app)
    app.run()

if __name__ == '__main__':
    app(target=main,assets_dir="assets")
    