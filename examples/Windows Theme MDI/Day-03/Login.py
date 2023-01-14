from flet import (
    Column,
    Container,
    ElevatedButton,
    Row,
    Text,
    colors,
    MainAxisAlignment,
    Padding,
    border,
    TextField,
    border_radius,
    ProgressRing,
    Margin
)

class Login(Container):
    def __init__(self,app,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # Container Prop
        self.app = app
        self.expand = True
        self.content = Column(
            [
                Row([self.UIBox()],alignment=MainAxisAlignment.CENTER)
            ],
            alignment=MainAxisAlignment.CENTER
        )

    def Auth(self,e):
        if self.user_name.value == "" or self.password.value == "":
            self.user_name.error_text = "Please provide username"
            self.password.error_text = "Please provide password"
            self.update()
            return
        else:
            from Auth.htpassAuth import Auth
            # Auth Logic in Here #
            self.loading.content = ProgressRing(scale=0.6)
            self.loading.update()
            
            auth = Auth(self.user_name.value,self.password.value)
            
            if auth.Login():
                self.page.client_storage.set('token',auth.token)
                self.app.session.auth = auth
                self.loading.content = Text("Login Successful.",color=colors.GREEN_400)
                self.loading.update()
                self.app.CheckLogin()
                return
            else:
                self.loading.content = Text("Wrong password.",color=colors.RED_400)
                self.loading.update()
                return

    def UIBox(self):
        #Login Page Data
        self.user_name = TextField(label="User name")
        self.password = TextField(label="Password", password=True)
        title = Container(Text("Auth Login",scale=3),padding=Padding(0,10,0,20))
        self.loading = Container()
        return Container(
            Column(
                [
                    Row (
                        [title],
                        alignment=MainAxisAlignment.CENTER
                    ),
                    Row (
                        [
                            Container(
                                Column(
                                    [
                                        self.user_name,
                                        self.password,
                                        Row(
                                            [
                                                ElevatedButton("Login",on_click=self.Auth),
                                                self.loading
                                            ],
                                            alignment=MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        
                                    ]
                                ),
                                bgcolor=colors.WHITE10,
                                expand=True,
                                border=border.all(1),
                                border_radius=border_radius.all(20),
                                padding=Padding(20,20,20,20)
                            )       
                        ]
                    )
                ]
            ),
            width  = 400,
            height = 450,
            margin = Margin(0,100,0,0)
        )
        
        

