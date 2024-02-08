from kivy.app import App
from kivymd.app import MDApp

from kivy.properties import StringProperty, ColorProperty

from kivy.lang.builder import Builder

from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField

from kivymd.uix.card import MDCard

# from kivy.uix.button import Button
# from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDTextButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.button import *

from kivy.uix.label import Label
from kivymd.uix.label import MDLabel

from kivy.uix.screenmanager import *
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.transition import *

from kivymd.uix.behaviors import DeclarativeBehavior, CommonElevationBehavior

from kivymd.uix.appbar import (
    MDTopAppBar,
    MDBottomAppBar,
    MDActionTopAppBarButton,
    MDActionBottomAppBarButton,
    MDTopAppBarLeadingButtonContainer
)

from kivymd.uix.navigationbar import *

from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog

from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.core.window import Window

import sqlite3

# from google_recaptcha import ReCaptcha
# from flask import Flask







# class Color:
#     Primary = "0560fa"
#     Secondary = "ec8000"
#     Success = "35b369"
#     Warning = "ebbc2e"
#     Info = "2f80ed"
#     Error = "ed3a3a"

#     Text1 = "141414"
#     Text2 = "3a3a3a"

#     Gray1 = "cfcfcf"
#     Gray2 = "a7a7a7"








class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

class MYProfileCard(MDCard, DeclarativeBehavior):
    def __init__(self, **kw):
        super(MYProfileCard, self).__init__(**kw)

    text_title = StringProperty()
    text_subtitle = StringProperty()
    icon = StringProperty()
    icon_color = ColorProperty()

# class MDTopAppBarElevated(MDTopAppBar):
#     def __init__(self, **kw):
#         super().__init__(**kw)
    



# app = Flask(__name__)
# recaptcha = ReCaptcha(app)

conn = sqlite3.connect('tunec.db')
cur = conn.cursor()
account_id = None
balance = float(0)
dark_mode = False

class LoginScreen(MDScreen):
    def __init__(self, **kw):
        super(LoginScreen, self).__init__(**kw)

        self.md_bg_color = self.theme_cls.backgroundColor

    def login_btn_click(self, *args):
        cur.execute(f"SELECT * FROM accounts WHERE username = \'{self.ids.username_input.text}\' AND password = \'{self.ids.password_input.text}\'")
        results = cur.fetchall()

        cur.execute(f"SELECT * FROM accounts WHERE email = \'{self.ids.username_input.text}\' AND password = \'{self.ids.password_input.text}\'")
        results_email = cur.fetchall()  

        if (len(results_email) > 0):
            results = results_email

        print(results)
        if (len(results) > 0 or len(results_email) > 0):
            print('-= Тунец =-\nАвторизация успешна!')

            #cur.execute(f"SELECT account_id FROM accounts WHERE email = \'{self.username_input.text}\' AND password = \'{self.password_input.text}\'")
            #account_id = cur.fetchone()

            global account_id
            account_id = results[0][0]
            print(f"account_id = {account_id}")

            #cur.execute(f"SELECT balance FROM accounts WHERE account_id = \'{account_id}\'")
            #global balance
            #balance = float(cur.fetchone()[0])

            HomeScreen.refresh_balance(HomeScreen(), args)
            print(f"balance = {balance}")

            self.ids.username_input.text = ''
            self.ids.password_input.text = ''

            #MobileApp.show_text_dialog('Авторизация', 'Вы успешно вошли в аккаунт')
            self.manager.current = 'home'
        else:
            show_text_dialog('Авторизация', 'Неправильный логин или пароль')

    def registration_btn_click(self, *args):
        self.manager.current = 'reg'
    
    def show_password(self, *args):
        if self.ids.password_input.password:
            self.ids.password_input.password = False
            self.ids.eye.icon = 'eye-outline'
        else:
            self.ids.password_input.password = True
            self.ids.eye.icon = 'eye-off-outline'

    def privacy_btn_click(self, *args):
        self.manager.current = 'privacy'

    def forgot_password_btn_click(self, *args):
        self.manager.current = 'forgot_password'
        









class RegScreen(MDScreen):
    def __init__(self, **kw):
        super(RegScreen, self).__init__(**kw)

        self.email_error = False

        self.md_bg_color = self.theme_cls.backgroundColor

    def privacy_label_click(self, w, touch):
        if w.collide_point(*touch.pos):
            self.manager.current = 'privacy'

    def back(self, w, touch):
        if w.collide_point(*touch.pos):
            self.manager.current = 'login'

    def reg_btn_click(self, instance):
        if self.email_error:
            show_text_dialog('Регистрация', 'Введён некорректный адрес эл. почты!')
        elif (self.ids.password_input.text != self.ids.password_confirm_input.text):
            show_text_dialog('Регистрация', 'Пароли не совпадают!')
        elif (len(self.ids.password_input.text) < 8):
            show_text_dialog('Регистрация', 'Длина пароля должна быть не менее 8!')
        elif (len(self.ids.password_input.text) > 12):
            show_text_dialog('Регистрация', 'Длина пароля должна быть не более 12!')
        elif not self.ids.privacy_chkbx.active:
            show_text_dialog('Регистрация', 'Вы должны принять наши условия использования и политику конфидециальности!')
        else:
            print('-= Тунец =-\nРегистрация успешна')

            account = (
                self.ids.username_input.text,
                self.ids.email_input.text,
                self.ids.password_input.text
            )

            cur.execute("INSERT INTO accounts(username, email, password) VALUES(?, ?, ?);", account)
            conn.commit()

            show_text_dialog('Регистрация', f'Пользователь {self.username_input.text} был успешно зарегестрирован в системе')
            
            self.ids.username_input.text = ''
            self.ids.email_input.text = ''
            self.ids.password_input.text = ''
            self.ids.password_confirm_input.text = ''
            
            self.email_error = False

            self.manager.current = 'login'

    def check_email(self, email):
        print('email = ' + email)

        has_uppercase = False
        for char in email:
            if char.isupper():
                has_uppercase = True
                break
        if not has_uppercase:
            if email.count('@') == 1:
                splitted_email = email.split('@')
                if splitted_email[1].count('.') == 1:
                    if len(splitted_email[0]) > 0 and len(splitted_email[1].split('.')[1]) > 0 and len(splitted_email[1].split('.')[0]) > 0:
                        self.ids.email_input.error = False
                        self.email_error = False
                    else:
                        self.ids.email_input.error = True
                        self.email_error = True
                else:
                    self.ids.email_input.error = True
                    self.email_error = True
            else:
                self.ids.email_input.error = True
                self.email_error = True
        else:
            self.ids.email_input.error = True
            self.email_error = True
        
        print(self.ids.email_input.error)

    def check_password_repeat(self, instance, password):
        pass















class HomeScreen(MDScreen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)

        self.ids.sm.current = "Home"

        self.balance = balance

        self.md_bg_color = self.theme_cls.backgroundColor
        self.hide_balance_bool = False

    def on_switch_tabs(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        self.ids.sm.current = item_text
        self.refresh_balance()

    def refresh_balance(self, *args):
        cur.execute(f"SELECT balance FROM accounts WHERE account_id = \'{account_id}\'")
        global balance
        if cur.fetchone() is not None:
            cur.execute(f"SELECT balance FROM accounts WHERE account_id = \'{account_id}\'")
            balance = float(cur.fetchone()[0])
            self.balance = balance
        else:
            self.balance = 0
        
        print(f"balance = {self.balance}")
        if self.hide_balance_bool:
            self.ids.balance_label.text = f"Ваш баланс:\n*****"
        else:
            self.ids.balance_label.text = f"Ваш баланс:\n${str(self.balance)}"

    def hide_balance(self, *args):
        self.hide_balance_bool = not self.hide_balance_bool

        self.refresh_balance(args[1])

    def dark_mode_switch(self, *args):
        global dark_mode
        dark_mode = not dark_mode
        print(f"Now dark_mode is {dark_mode}")

    def logout(self, *args):
        self.manager.current = "login"





















class ForgotPasswordScreen(MDScreen):
    def __init__(self, **kw):
        super(ForgotPasswordScreen, self).__init__(**kw)

        self.md_bg_color = self.theme_cls.backgroundColor

    def back(self, w, touch):
        pass

    def send_btn_click(self, instance):
        pass





















class OPTVerificationScreen(MDScreen):
    def __init__(self, **kw):
        super(OPTVerificationScreen, self).__init__(**kw)

        self.md_bg_color = self.theme_cls.backgroundColor

    def send_btn_click(self, instance):
        pass

    def back(self):
        pass


















class NewPasswordScreen(MDScreen):
    def __init__(self, **kw):
        super(NewPasswordScreen, self).__init__(**kw)

        self.md_bg_color = self.theme_cls.backgroundColor

    def change_btn_click(self, instance):
        pass

    def check_password_repeat(self, instance, password):
        pass

    def back(self):
        pass



















class PrivacyScreen(MDScreen):
    def __init__(self, **kw):
        super(PrivacyScreen, self).__init__(**kw)

        self.md_bg_color = self.theme_cls.backgroundColor

    def back(self):
        pass


















class MobileApp(MDApp):
    Primary = "0560fa"
    Secondary = "ec8000"
    Success = "35b369"
    Warning = "ebbc2e"
    Info = "2f80ed"
    Error = "ed3a3a"

    Text1 = "141414"
    Text2 = "3a3a3a"

    Gray1 = "cfcfcf"
    Gray2 = "a7a7a7"

    colors = {
        "Primary": "0560fa",
        "Gray1": "cfcfcf",
        "Gray2": "a7a7a7",
        "Warning": "ebbc2e",
        "Error": "ed3a3a"
        }

    def build(self):
        Window.size = (360, 800)
        # Window.size = (600, 800)

        cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT,
                balance REAL);
                """)
        conn.commit()

        # self.theme_cls.material_style = "M2"
        self.theme_cls.theme_style = "Light"
        # self.theme_cls.primary_palette = "Olive"
        self.theme_cls.theme_style_switch_animation = False

        Builder.load_file('MYProfileCard.kv')
        Builder.load_file('LoginScreen.kv')
        Builder.load_file('RegScreen.kv')
        Builder.load_file('HomeScreen.kv')

        sm = MDScreenManager(transition = FadeTransition())
        sm.add_widget(HomeScreen(name = 'home'))
        sm.add_widget(LoginScreen(name = 'login'))
        sm.add_widget(RegScreen(name = 'reg'))
        sm.add_widget(PrivacyScreen(name = 'privacy'))
        sm.add_widget(ForgotPasswordScreen(name = 'forgot_password'))
        sm.add_widget(OPTVerificationScreen(name = 'opt_verification'))
        sm.add_widget(NewPasswordScreen(name = 'new_password'))

        return sm

    # def on_start(self):
    #     def on_start(*args):
    #         self.root.md_bg_color = self.theme_cls.backgroundColor





def show_text_dialog(title_, text_):
    # dialog = MDDialog(
    #     title = title_,
    #     text = text_
    # )
    # dialog.open()
    pass









if __name__ == '__main__':
    MobileApp().run()