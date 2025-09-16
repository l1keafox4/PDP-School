import flet as ft

def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text("Hello my first Flet app")))


ft.app(main)