from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons

KV = '''
<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: "#4a4939"
    icon_color: "#4a4939"
    focus_behavior: False
    selected_color: "#4a4939"
    _no_ripple_effect: True


MDScreen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDTopAppBar:
                    title: "Navbar"
                    elevation: 4
                    pos_hint: {"top": 1}
                    md_bg_color: "#e7e4c0"
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerLabel:
                    text: "Registers"

                DrawerClickableItem:
                    icon: "car-brake-parking"
                    text: "Checkin"

                DrawerClickableItem:
                    icon: "car"
                    text: "Checkout"
'''


class Navbar(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red" 
        return Builder.load_string(KV)


Navbar().run()