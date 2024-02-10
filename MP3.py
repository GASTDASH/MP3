from kivy.app import App
from kivymd.app import MDApp

from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ColorProperty, BooleanProperty
from kivymd.uix.behaviors import CommonElevationBehavior

from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField

from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDTextButton, MDFloatingActionButton, MDIconButton

from kivy.uix.label import Label
from kivymd.uix.label import MDLabel

from kivy.uix.screenmanager import *
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.transition import *

from kivymd.uix.card import MDCard

from kivymd.uix.toolbar import MDTopAppBar

from kivymd.uix.bottomnavigation import *

from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog

from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.core.window import Window

import sqlite3
import time

from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha

import io

from plyer import notification


conn = sqlite3.connect('tunec.db')
cur = conn.cursor()
account_id = None
balance = float(0)
dark_mode = False


class MYProfileCard(MDCard):
    text_title = StringProperty()
    text_subtitle = StringProperty()
    icon = StringProperty()
    icon_color = ColorProperty()

    def __init__(self, **kw):
        super(MYProfileCard, self).__init__(**kw)


class MYTopBar(MDCard):
    title = StringProperty()
    back = BooleanProperty()

    def __init__(self, **kw):
        super(MYTopBar, self).__init__(**kw)


class MYSearchTextField(MDCard):
    hint_text = StringProperty()

    def __init__(self, **kw):
        super(MYSearchTextField, self).__init__(**kw)


class MYHomeServiceCard(MDCard):
    text_title = StringProperty()
    text_subtitle = StringProperty()
    icon = StringProperty()

    def __init__(self, **kw):
        super(MYHomeServiceCard, self).__init__(**kw)

    def touch_down(self, w, touch):
        if w.collide_point(*touch.pos):
            self.md_bg_color = Color.Primary
            self.ids.title.text_color = "#ffffff"
            self.ids.subtitle.text_color = "#ffffff"
            self.ids.icon.text_color = "#ffffff"

    def touch_up(self, *args):
        self.md_bg_color = "#f2f2f2"
        self.ids.title.text_color = Color.Primary
        self.ids.subtitle.text_color = "#000000"
        self.ids.icon.text_color = Color.Primary


class LoginScreen(MDScreen):
    def __init__(self, **kw):
        super(LoginScreen, self).__init__(**kw)
        
    def login_btn_click(self, *args):
        cur.execute(f"SELECT * FROM accounts WHERE username = \'{self.ids.username_input.text}\' AND password = \'{self.ids.password_input.text}\'")
        results = cur.fetchall()

        cur.execute(f"SELECT * FROM accounts WHERE email = \'{self.ids.username_input.text}\' AND password = \'{self.ids.password_input.text}\'")
        results_email = cur.fetchall()  

        if (len(results_email) > 0):
            results = results_email

        print("[G_DEBUG] ")
        print(results)
        if (len(results) > 0 or len(results_email) > 0):
            print('[G_DEBUG] Authorization successful!')

            #cur.execute(f"SELECT account_id FROM accounts WHERE email = \'{self.username_input.text}\' AND password = \'{self.password_input.text}\'")
            #account_id = cur.fetchone()

            global account_id
            account_id = results[0][0]
            print(f"[G_DEBUG] account_id = {account_id}")

            #cur.execute(f"SELECT balance FROM accounts WHERE account_id = \'{account_id}\'")
            #global balance
            #balance = float(cur.fetchone()[0])

            HomeScreen.update_balance(HomeScreen(), args)
            print(f"[G_DEBUG] balance = {balance}")

            self.ids.username_input.text = ''
            self.ids.password_input.text = ''

            #MobileApp.show_text_dialog('Авторизация', 'Вы успешно вошли в аккаунт')
            self.manager.current = 'home'
        else:
            show_text_dialog('Авторизация', 'Неправильный логин или пароль')

    def registration_btn_click(self, instance):
        self.manager.current = 'reg'

    # def show_password(self, instance):
    #     self.password_input.password = not self.password_input.password
    def show_password(self, instance):
        if self.ids.password_input.password:
            self.ids.password_input.password = False
            self.ids.eye.icon = 'eye-outline'
        else:
            self.ids.password_input.password = True
            self.ids.eye.icon = 'eye-off-outline'

    def privacy_btn_click(self, instance):
        self.manager.current = 'privacy'

    def forgot_password_btn_click(self, instance):
        self.manager.current = 'forgot_password'
        # notification.notify('Some title', 'Some message text')


class RegScreen(MDScreen):
    def __init__(self, **kw):
        super(RegScreen, self).__init__(**kw)

        self.email_error = False

        # Window.bind(on_keyboard = self.back)

        cur.execute("SELECT * FROM accounts;")
        result = cur.fetchall()
        print("[G_DEBUG] ")
        print(result)

    def privacy_label_click(self, w, touch):
        if w.collide_point(*touch.pos):
            self.manager.current = 'privacy'

    def back(self, w, touch):
        if w.collide_point(*touch.pos):
            self.manager.current = 'login'

    def reg_btn_click(self, instance):
        if self.ids.username_input.text == "":
            show_text_dialog('Регистрация', 'Вы не ввели имя пользователя!')
        elif self.ids.email_input.text == "":
            show_text_dialog('Регистрация', 'Вы не ввели адрес эл. почты!')
        elif self.email_error:
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
            print('[G_DEBUG] Registration successful!')

            account = (
                self.ids.username_input.text,
                self.ids.email_input.text,
                self.ids.password_input.text
            )

            cur.execute("INSERT INTO accounts(username, email, password, balance) VALUES(?, ?, ?, 0.0);", account)
            conn.commit()

            show_text_dialog('Регистрация', f'Пользователь {self.ids.username_input.text} был успешно зарегестрирован в системе')
            
            self.ids.username_input.text = ''
            self.ids.email_input.text = ''
            self.ids.password_input.text = ''
            self.ids.password_confirm_input.text = ''
            
            self.email_error = False

            self.manager.current = 'login'

    def check_email(self, email):
        print('[G_DEBUG] email = ' + email)

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
        print('[G_DEBUG] password = ' + password)

        if self.password_confirm_input.text == self.password_input.text:
            self.password_confirm_input.error = False
        else:
            self.password_confirm_input.error = True


class HomeScreen(MDScreen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)

        self.balance = balance
        self.hide_balance_bool = False

    def on_open(self, *args):
        self.update_balance(args)
        self.update_avatar(args)
        self.update_username(args)

    def update_avatar(self, *args):
        self.ids.avatar.source = './assets/avatar.png'
    
    def update_username(self, *args):
        cur.execute(f"SELECT username FROM accounts WHERE account_id = \'{account_id}'")
        result = cur.fetchone()
        if result is not None:
            self.ids.username_label.text = f"Hello {result[0]}"
        else:
            self.ids.username_label.text = "Username ERROR"

    def update_balance(self, *args):
        cur.execute(f"SELECT balance FROM accounts WHERE account_id = \'{account_id}\'")
        global balance
        res = cur.fetchone()
        if res is not None:
            if res[0] is not None:
                balance = float(res[0])
                self.balance = balance
        else:
            self.balance = 0
        
        print(f"[G_DEBUG] balance = {self.balance}")
        if self.hide_balance_bool:
            self.ids.balance_label.text = f"Ваш баланс: *****"
        else:
            self.ids.balance_label.text = f"Ваш баланс: [color={Color.Primary}][b]${str(self.balance)}[/b][/color]"

    def hide_balance(self, *args):
        self.hide_balance_bool = not self.hide_balance_bool

        self.update_balance(args)

    def dark_mode_switch(self, *args):
        global dark_mode
        dark_mode = not dark_mode
        print(f"[G_DEBUG] Now dark_mode is {dark_mode}")

    def logout(self, *args):
        self.ids.navigator.switch_tab("home")
        self.manager.current = "login"


class AddPaymentMethodScreen(MDScreen):
    def __init__(self, **kw):
        super(AddPaymentMethodScreen, self).__init__(**kw)

        self.ids.topbar.ids.back_btn.bind(on_release = self.back)

    def back(self, *args):
        self.manager.current = 'home'


class ForgotPasswordScreen(MDScreen):
    def __init__(self, **kw):
        super(ForgotPasswordScreen, self).__init__(**kw)

    def back(self, w, touch):
        # print(touch.pos)
        # self.do_layout()
        # print(self.back_label.size)
        # print(self.back_label.pos)
        if w.collide_point(*touch.pos):
            self.manager.current = 'login'
            

    def send_btn_click(self, instance):
        cur.execute(f"SELECT account_id FROM accounts WHERE email = \'{self.ids.email_input.text}\'")
        results = cur.fetchone()

        print('[G_DEBUG] \n', results)
        
        if len(results) > 0:
            global account_id
            account_id = results[0]
            print(f"[G_DEBUG] account_id = {account_id}")
            self.manager.current = 'opt_verification'
        else:
            show_text_dialog("OPT Verification", "Данный адрес эл. почты не зарегистрирован")


class OPTVerificationScreen(MDScreen):
    def __init__(self, **kw):
        super(OPTVerificationScreen, self).__init__(**kw)

    def send_btn_click(self, instance):
        self.manager.current = 'new_password'

    def back(self):
        self.manager.current = 'forgot_password'


class NewPasswordScreen(MDScreen):
    def __init__(self, **kw):
        super(NewPasswordScreen, self).__init__(**kw)

    def change_btn_click(self, *args):
        if not self.check_password_repeat(args):
            password = str(self.ids.password_input.text)
            global account_id
            cur.execute(f"UPDATE accounts SET password = \'{password}\' WHERE account_id = \'{account_id}\'")
            conn.commit()
            self.manager.current = 'home'

    def check_password_repeat(self, *args):
        print('[G_DEBUG] password = ' + self.ids.password_input.text)

        if self.ids.password_confirm_input.text == self.ids.password_input.text:
            self.ids.password_confirm_input.error = False
            return False
        else:
            self.ids.password_confirm_input.error = True
            return True

    # def back(self):
    #     self.manager.current = 'forgot_password'


class PrivacyScreen(MDScreen):
    def __init__(self, **kw):
        super(PrivacyScreen, self).__init__(**kw)

        # privacy_text = str()
        # with open('./privacy.ini', 'r') as file:
        #     privacy_text = file.read()
        with io.open('./privacy.ini', encoding='utf-8') as file:
            privacy_text = file.read()

        self.scrollview = MDScrollView(
            do_scroll_x = False,
            do_scroll_y = True,
            size_hint = (1, None),
            size = (Window.width, Window.height)
        )
        self.add_widget(self.scrollview)

        # self.privacy_label = Label(
        #     text = privacy_text,
        #     color = 'black',
        #     markup = True,
        #     size_hint = (1, None),
        #     # pos_hint = {'center_x': .5}
        # )
        # self.privacy_label.texture_update()
        # # print(self.privacy_label.texture_size)
        # self.privacy_label.text_size[0] = self.scrollview.size[0]
        # self.privacy_label.height = self.privacy_label.texture_size[1] + 1000
        # self.scrollview.add_widget(self.privacy_label)

        self.grid = MDGridLayout(
            size_hint = (1, None),
            cols = 1,
            # height = 3400 * (500 / Window.width),
            padding = 20
        )
        self.grid.bind(minimum_height = self.grid.setter('height'))

        self.privacy_label = MDLabel(
            text = privacy_text,
            markup = True,
            # height = 3400 * (500 / Window.width),
            size_hint = (1, None)
        )
        # self.privacy_label.texture_update()
        # print(f"self.privacy_label.texture_size = {self.privacy_label.texture_size}")
        # self.privacy_label.height = self.privacy_label.texture_size[1]
        self.privacy_label.bind(texture_size = lambda instance, size: setattr(self.privacy_label, "height", size[1] + 400))
        self.grid.add_widget(self.privacy_label)
        self.scrollview.add_widget(self.grid)

        self.toolbar = MDTopAppBar(
            title = "Privacy Policy",
            pos_hint = {"top": 1},
            left_action_items=[["arrow-left", lambda x: self.back()]]
        )
        self.add_widget(self.toolbar)

    def back(self):
        self.manager.current = 'reg'


class Color:
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


class MobileApp(MDApp):
    colors = {
            "Primary": "#0560fa",
            "Secondary": "e#c8000",
            "Success": "#35b369",
            "Warning": "#ebbc2e",
            "Info": "#2f80ed",
            "Error": "#ed3a3a",
            "Text1": "#141414",
            "Text2": "#3a3a3a",
            "Gray1": "#cfcfcf",
            "Gray2": "#a7a7a7"
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

        self.theme_cls.material_style = "M2"

        Builder.load_file('MYProfileCard.kv')
        Builder.load_file('MYTopBar.kv')
        Builder.load_file('MYSearchTextField.kv')
        Builder.load_file('MYHomeServiceCard.kv')

        Builder.load_file('LoginScreen.kv')
        Builder.load_file('HomeScreen.kv')
        Builder.load_file('RegScreen.kv')
        Builder.load_file('AddPaymentMethodScreen.kv')
        Builder.load_file('ForgotPasswordScreen.kv')
        Builder.load_file('OPTVerificationScreen.kv')
        Builder.load_file('NewPasswordScreen.kv')

        sm = MDScreenManager(transition = FadeTransition())
        sm.add_widget(HomeScreen(name = 'home'))
        sm.add_widget(LoginScreen(name = 'login'))
        sm.add_widget(RegScreen(name = 'reg'))
        sm.add_widget(PrivacyScreen(name = 'privacy'))
        sm.add_widget(ForgotPasswordScreen(name = 'forgot_password'))
        sm.add_widget(OPTVerificationScreen(name = 'opt_verification'))
        sm.add_widget(NewPasswordScreen(name = 'new_password'))
        sm.add_widget(AddPaymentMethodScreen(name = 'add_payment_method'))
        return sm

def show_text_dialog(title_, text_):
    dialog = MDDialog(
        title = title_,
        text = text_
    )
    dialog.open()

if __name__ == '__main__':
    MobileApp().run()