import flet as ft
mousePosPreviousTick: list[float] = None
def main(page: ft.Page):
    def on_pan_update1(e: ft.DragUpdateEvent):
        c.top = max(0, c.top + e.delta_y)
        c.left = max(0, c.left + e.delta_x)
        c.update()

    def on_pan_update2(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()
        
    def on_pan_update_window(e: ft.DragUpdateEvent):
        page: ft.Page = e.page
        page.window_top += e.delta_y
        page.window_left += e.delta_x
        page.update()

    # def on_pan_update_window(e: ft.DragUpdateEvent):
    #     import mouse
    #     global mousePosPreviousTick
    #     if mousePosPreviousTick != None:
    #         page: ft.Page = e.page
    #         page.window_top +=  mouse.get_position()[1] - mousePosPreviousTick[1]
    #         page.window_left += mouse.get_position()[0] - mousePosPreviousTick[0]
    #     mousePosPreviousTick = mouse.get_position()
    #     page.update()

    gd = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=50,
        on_pan_update=on_pan_update1,
    )

    c = ft.Container(gd, bgcolor=ft.colors.AMBER, width=50, height=50, left=0, top=0)

    gd1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_vertical_drag_update=on_pan_update2,
        left=100,
        top=100,
        content=ft.Container(bgcolor=ft.colors.BLUE, width=50, height=50),
    )

    gd_window = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_vertical_drag_update=on_pan_update_window,
        # , on_pan_end=self.resizeWindowDragHandlesEND
        left=200,
        top=200,
        content=ft.Container(bgcolor=ft.colors.PINK, width=50, height=50),
    )

    page.add( ft.Stack([c, gd1, gd_window], width=1000, height=500))

ft.app(target=main)