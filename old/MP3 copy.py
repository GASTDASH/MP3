from kivy.app import App
from kivymd.app import MDApp

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

from kivymd.uix.toolbar import MDTopAppBar

from kivymd.uix.bottomnavigation import *

from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog

from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.core.window import Window

import sqlite3

# from google_recaptcha import ReCaptcha
# from flask import Flask







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

        self.add_widget(
            MDLabel(
                text = 'Welcome back',
                font_style = 'H4',
                # halign = "center",
                size_hint = (1, None),
                pos_hint = {'top': .88},
                padding = 20
            )
        )
        self.add_widget(
            MDLabel(
                text = 'Fill in your email/username and password to continue',
                font_style = 'Subtitle2',
                theme_text_color = "Custom",
                text_color = Color.Gray2,
                size_hint = (1, None),
                pos_hint = {'top': .81},
                padding = 20
            )
        )

        self.username_input = MDTextField(
            hint_text = 'Username / Email',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.56},
            mode = 'rectangle'
        )
        self.add_widget(self.username_input)

        self.password_input = MDTextField(
            hint_text = 'Password',
            #font_size = 24,
            password = True,
            password_mask = '*',
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.45},
            mode = 'rectangle'
        )
        self.add_widget(self.password_input)
        
        # self.show_password_chbox = MDCheckbox(
        #     size_hint = (None, None),
        #     size = ("48dp", "48dp"),
        #     pos_hint = {'center_x': 0.9, 'center_y': 0.53}
        # )
        # self.show_password_chbox.bind(on_release = self.show_password)
        # self.add_widget(self.show_password_chbox)
        self.show_password_btn = MDIconButton(
            size_hint = (None, None),
            size = ("48dp", "48dp"),
            pos_hint = {'center_x': .87, 'center_y': .49},
            icon = 'eye-off-outline',
        )
        self.show_password_btn.bind(on_release = self.show_password)
        self.add_widget(self.show_password_btn)

        self.login_btn = MDRaisedButton(
            text = 'Log In',
            md_bg_color = Color.Primary,
            size_hint = (.7, .08),
            pos_hint = {'center_x': 0.5, 'y': 0.3}
        )
        self.login_btn.bind(on_release = self.login_btn_click)
        self.add_widget(self.login_btn)

        self.registration_btn = MDRectangleFlatButton(
            text = 'No account?',
            line_color = Color.Primary,
            size_hint = (.3, .06),
            pos_hint = {'center_x': 0.5, 'y': 0.19}
        )
        self.registration_btn.bind(on_release = self.registration_btn_click)
        self.add_widget(self.registration_btn)

        # self.privacy_btn = MDTextButton(
        #     text = 'Privacy Policy',
        #     theme_text_color = "Custom",
        #     text_color = Color.Primary,
        #     pos_hint = {'center_x': 0.5, 'y': 0.04}
        # )
        # self.privacy_btn.bind(on_release = self.privacy_btn_click)
        # self.add_widget(self.privacy_btn)

        self.forgot_password_btn = MDTextButton(
            text = 'Forgot password',
            theme_text_color = "Custom",
            text_color = Color.Primary,
            pos_hint = {'center_x': 0.5, 'y': 0.1}
        )
        self.forgot_password_btn.bind(on_release = self.forgot_password_btn_click)
        self.add_widget(self.forgot_password_btn)

    def login_btn_click(self, instance):
        # if recaptcha.verify():
        #     print('ReCaptcha has successded')
        # else:
        #     print('ReCaptcha has failed')

        cur.execute(f"SELECT * FROM accounts WHERE username = \'{self.username_input.text}\' AND password = \'{self.password_input.text}\'")
        results = cur.fetchall()

        cur.execute(f"SELECT * FROM accounts WHERE email = \'{self.username_input.text}\' AND password = \'{self.password_input.text}\'")
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

            HomeScreen.refresh_balance(HomeScreen(), instance)
            print(f"balance = {balance}")

            self.username_input.text = ''
            self.password_input.text = ''

            #MobileApp.show_text_dialog('Авторизация', 'Вы успешно вошли в аккаунт')
            self.manager.current = 'home'
        else:
            show_text_dialog('Авторизация', 'Неправильный логин или пароль')

    def registration_btn_click(self, instance):
        self.manager.current = 'reg'

    # def show_password(self, instance):
    #     self.password_input.password = not self.password_input.password
    def show_password(self, instance):
        if self.password_input.password:
            self.password_input.password = False
            self.show_password_btn.icon = 'eye-outline'
        else:
            self.password_input.password = True
            self.show_password_btn.icon = 'eye-off-outline'

    def privacy_btn_click(self, instance):
        self.manager.current = 'privacy'

    def forgot_password_btn_click(self, instance):
        self.manager.current = 'forgot_password'
        









class RegScreen(MDScreen):
    def __init__(self, **kw):
        super(RegScreen, self).__init__(**kw)

        self.email_error = False

        # Window.bind(on_keyboard = self.back)

        cur.execute("SELECT * FROM accounts;")
        result = cur.fetchall()
        print(result)

        self.add_widget(
            MDLabel(
                text = 'Create an account',
                font_style = 'H4',
                # halign = "center",
                size_hint = (1, None),
                pos_hint = {'top': .94},
                padding = 20
            )
        )
        self.add_widget(
            MDLabel(
                text = 'Complete the sign up process to get started',
                font_style = 'Subtitle2',
                theme_text_color = "Custom",
                text_color = Color.Gray2,
                size_hint = (1, None),
                pos_hint = {'top': .88},
                padding = 20
            )
        )

        self.username_input = MDTextField(
            hint_text = 'Username',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.67},
            #foreground_color = (0, 0, 0, 255),
            error_color = (255, 0, 0, 255),
            mode = 'rectangle'
        )
        self.add_widget(self.username_input)

        self.email_input = MDTextField(
            hint_text = 'Email',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.56},
            #foreground_color = (0, 0, 0, 255),
            error_color = (255, 0, 0),
            mode = 'rectangle'
        )
        self.email_input.bind(text = self.check_email)
        self.add_widget(self.email_input)
        
        self.password_input = MDTextField(
            hint_text = 'Password',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.45},
            #foreground_color = (0, 0, 0, 255),
            error_color = (255, 0, 0),
            mode = 'rectangle'
        )
        self.password_input.bind(text = self.check_password_repeat)
        self.add_widget(self.password_input)
        
        self.password_confirm_input = MDTextField(
            hint_text = 'Password confirm',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.34},
            #foreground_color = (0, 0, 0, 255),
            error_color = (255, 0, 0),
            mode = 'rectangle'
        )
        self.password_confirm_input.bind(text = self.check_password_repeat)
        self.add_widget(self.password_confirm_input)

        self.privacy_label = MDLabel(
            markup = True,
            text = f"[color={str.upper(Color.Gray2)}]By ticking this box, you are agree to our [color={str.upper(Color.Warning)}]Terms and conditions and privacy policy[/color]",
            font_style = 'Subtitle2',
            halign = 'center',
            size_hint = (.7, .04),
            pos_hint = {'center_x': .5, 'top': .3}
        )
        self.privacy_label.bind(on_touch_down = self.privacy_label_click)
        self.add_widget(self.privacy_label)

        self.privacy_chkbx = MDCheckbox(
            size_hint = (None, None),
            size = ("48dp", "48dp"),
            pos_hint = {'center_x': .1, 'center_y': .3}
        )
        self.add_widget(self.privacy_chkbx)

        self.reg_btn = MDRaisedButton(
            text = 'Sign Up',
            md_bg_color = Color.Primary,
            size_hint = (.9, .06),
            pos_hint = {'center_x': 0.5, 'center_y': 0.18}
        )
        self.reg_btn.bind(on_release = self.reg_btn_click)
        self.add_widget(self.reg_btn)

        # self.back_btn = MDRectangleFlatButton(
        #     text = "<-",
        #     size_hint = (.08, .08),
        #     pos_hint = {'x': .1, 'y': .1}
        # )
        # self.back_btn = MDIconButton(
        #     icon = "arrow-left",
        #     theme_icon_color = "Custom",
        #     icon_color = Color.Primary,
        #     pos_hint = {'x': .02, 'center_y': .15}
        # )
        # self.back_btn.bind(on_release = self.back_btn_click)
        # self.add_widget(self.back_btn)

        self.back_label = MDLabel(
            markup = True,
            text = f"[color={str.upper(Color.Gray2)}]Already have an account? [color={str.upper(Color.Primary)}]Sign in[/color]",
            font_style = 'Subtitle1',
            halign = 'center',
            size_hint = (1, .04),
            pos_hint = {'top': .1}
        )
        self.back_label.bind(on_touch_down = self.back)
        self.add_widget(self.back_label)

    # def back(self, window, key, *largs):
    #     if key == 27:
    #         self.manager.current = 'login'

    def privacy_label_click(self, w, touch):
        if w.collide_point(*touch.pos):
            self.manager.current = 'privacy'

    def back(self, w, touch):
        if w.collide_point(*touch.pos):
            self.manager.current = 'login'

    def reg_btn_click(self, instance):
        if self.email_error:
            show_text_dialog('Регистрация', 'Введён некорректный адрес эл. почты!')
        elif (self.password_input.text != self.password_confirm_input.text):
            show_text_dialog('Регистрация', 'Пароли не совпадают!')
        elif (len(self.password_input.text) < 8):
            show_text_dialog('Регистрация', 'Длина пароля должна быть не менее 8!')
        elif (len(self.password_input.text) > 12):
            show_text_dialog('Регистрация', 'Длина пароля должна быть не более 12!')
        elif not self.privacy_chkbx.active:
            show_text_dialog('Регистрация', 'Вы должны принять наши условия использования и политику конфидециальности!')
        else:
            print('-= Тунец =-\nРегистрация успешна')

            account = (
                self.username_input.text,
                self.email_input.text,
                self.password_input.text
            )

            cur.execute("INSERT INTO accounts(username, email, password) VALUES(?, ?, ?);", account)
            conn.commit()

            show_text_dialog('Регистрация', f'Пользователь {self.username_input.text} был успешно зарегестрирован в системе')
            
            self.username_input.text = ''
            self.email_input.text = ''
            self.password_input.text = ''
            self.password_confirm_input.text = ''
            
            self.email_error = False

            self.manager.current = 'login'

    def check_email(self, instance, email):
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
                        self.email_input.error = False
                        self.email_error = False
                    else:
                        self.email_input.error = True
                        self.email_error = True
                else:
                    self.email_input.error = True
                    self.email_error = True
            else:
                self.email_input.error = True
                self.email_error = True
        else:
            self.email_input.error = True
            self.email_error = True

    def check_password_repeat(self, instance, password):
        print('password = ' + password)

        if self.password_confirm_input.text == self.password_input.text:
            self.password_confirm_input.error = False
        else:
            self.password_confirm_input.error = True















class HomeScreen(MDScreen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)

        self.hide_balance_bool = False

        self.toolbar = MDTopAppBar(
            title = "Forgot Password",
            pos_hint = {"top": 1},
            left_action_items=[["arrow-left", lambda x: self.back()]]
        )
        self.add_widget(self.toolbar)

        self.navigator = MDBottomNavigation(
            panel_color = '#ffffff',
            pos_hint = {"bottom": 0}
        )

        self.home_tab = MDBottomNavigationItem(
            name = "home",
            text = "Home",
            icon = "home"
        )
        self.home_tab.add_widget(MDLabel(text = "It's a Home screen"))

        self.wallet_tab = MDBottomNavigationItem(
            name = "wallet",
            text = "Wallet",
            icon = "wallet"
        )
        self.wallet_tab.add_widget(MDLabel(text = "It's a Wallet screen"))

        self.track_tab = MDBottomNavigationItem(
            name = "track",
            text = "Track",
            icon = "car"
        )
        self.track_tab.add_widget(MDLabel(text = "It's a Track screen"))

        self.profile_tab = MDBottomNavigationItem(
            name = "profile",
            text = "Profile",
            icon = "account-circle"
        )
        self.profile_tab.bind(on_enter = self.refresh_balance)
        
        self.balance_label = MDLabel(font_style = "H3", text = f"Ваш баланс:\n${balance}", pos_hint = {"center_x": .5, "top": 1}, size_hint = (.8, .3))
        self.profile_tab.add_widget(self.balance_label)

        self.profile_stacklayout = MDStackLayout(spacing = (10, 10), padding = (0, 200, 0, 0))
        
        self.refresh_button = MDRectangleFlatButton(text = "Обновить баланс", size_hint = (1, None))
        self.refresh_button.bind(on_release = self.refresh_balance)
        self.profile_stacklayout.add_widget(self.refresh_button)

        self.hide_button = MDRectangleFlatButton(text = "Скрыть/показать баланс", size_hint = (1, None))
        self.hide_button.bind(on_release = self.hide_balance)
        self.profile_stacklayout.add_widget(self.hide_button)

        self.card_settings_button = MDRectangleFlatButton(text = "Настройки карты и банковского аккаунта", size_hint = (1, None))
        self.profile_stacklayout.add_widget(self.card_settings_button)

        self.dark_mode_button = MDRectangleFlatButton(text = "Вкл/выкл тёмный режим", size_hint = (1, None))
        self.dark_mode_button.bind(on_release = self.dark_mode_switch)
        self.profile_stacklayout.add_widget(self.dark_mode_button)

        self.logout_button = MDRectangleFlatButton(text = "Выйти из аккаунта", size_hint = (1, None))
        self.logout_button.bind(on_release = self.logout)
        self.profile_stacklayout.add_widget(self.logout_button)

        self.profile_tab.add_widget(self.profile_stacklayout)


        self.navigator.add_widget(self.home_tab)
        self.navigator.add_widget(self.wallet_tab)
        self.navigator.add_widget(self.track_tab)
        self.navigator.add_widget(self.profile_tab)
        
        self.add_widget(self.navigator)

    def refresh_balance(self, instance):
        cur.execute(f"SELECT balance FROM accounts WHERE account_id = \'{account_id}\'")
        global balance
        balance = float(cur.fetchone()[0])
        
        print(f"balance = {balance}")
        if self.hide_balance_bool:
            self.balance_label.text = f"Ваш баланс:\n*****"
        else:
            self.balance_label.text = f"Ваш баланс:\n${str(balance)}"

    def hide_balance(self, instance):
        self.hide_balance_bool = not self.hide_balance_bool

        self.refresh_balance(instance)

    def dark_mode_switch(self, instance):
        global dark_mode
        dark_mode = not dark_mode
        print(f"Now dark_mode is {dark_mode}")

    def logout(self, instance):
        # self.manager.get_screen('login').username_input.text = ""
        # self.manager.get_screen('login').password_input.text = ""

        self.manager.current = "login"





















class ForgotPasswordScreen(MDScreen):
    def __init__(self, **kw):
        super(ForgotPasswordScreen, self).__init__(**kw)

        # self.toolbar = MDTopAppBar(
        #     title = "Forgot Password",
        #     pos_hint = {"top": 1},
        #     left_action_items=[["arrow-left", lambda x: self.back()]]
        # )
        # self.add_widget(self.toolbar)

        self.add_widget(
            MDLabel(
                text = 'Forgot Password',
                font_style = 'H4',
                # halign = "center",
                size_hint = (1, None),
                pos_hint = {'top': .88},
                padding = 20
            )
        )
        self.add_widget(
            MDLabel(
                text = 'Enter your email address',
                font_style = 'Subtitle2',
                theme_text_color = "Custom",
                text_color = Color.Gray2,
                size_hint = (1, None),
                pos_hint = {'top': .82},
                padding = 20
            )
        )

        self.email_input = MDTextField(
            hint_text = 'Email Address',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.56},
            #foreground_color = (0, 0, 0, 255),
            error_color = (255, 0, 0),
            mode = 'rectangle'
        )
        self.add_widget(self.email_input)

        self.send_btn = MDRaisedButton(
            text = 'Send OPT',
            md_bg_color = Color.Primary,
            size_hint = (.7, .08),
            pos_hint = {'center_x': 0.5, 'y': 0.3}
        )
        self.send_btn.bind(on_release = self.send_btn_click)
        self.add_widget(self.send_btn)

        self.back_label = MDLabel(
            markup = True,
            text = f"[color={str.upper(Color.Gray2)}]Remember password? Back to [color={str.upper(Color.Primary)}]Sign in[/color]",
            font_style = 'Subtitle1',
            halign = 'center',
            size_hint = (1, .04),
            pos_hint = {'top': .2}
        )
        self.back_label.bind(on_touch_down = self.back)
        self.add_widget(self.back_label)
        # self.back_label = MDLabel(
        #     text = 'Remember password? Back to',
        #     font_style = 'Subtitle1',
        #     halign = 'center',
        #     theme_text_color = "Custom",
        #     text_color = Color.Gray2,
        #     size_hint = (1, .1),
        #     pos_hint = {'top': .2, 'x': -.1},
        # )
        # self.add_widget(self.back_label)
        # print(f"pos1 = {self.back_label.pos}")
        # self.do_layout()
        # print(f"pos2 = {self.back_label.pos}")
        # self.back_btn = MDLabel(
        #     text = 'Sign in',
        #     font_style = 'Subtitle1',
        #     halign = 'center',
        #     theme_text_color = "Custom",
        #     text_color = Color.Primary,
        #     size_hint = (1, .1),
        #     pos_hint = {'top': .2},
        #     pos = (self.back_label.pos[0] + 110, self.back_label.pos[1])
        # )
        # self.back_btn.bind(on_release = self.back)
        # self.add_widget(self.back_btn)

    def back(self, w, touch):
        # print(touch.pos)
        # self.do_layout()
        # print(self.back_label.size)
        # print(self.back_label.pos)
        if w.collide_point(*touch.pos):
            self.manager.current = 'login'
            

    def send_btn_click(self, instance):
        cur.execute(f"SELECT * FROM accounts WHERE email = \'{self.email_input.text}\'")
        results = cur.fetchall()

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n', results)
        
        if len(results) > 0:
            self.manager.current = 'opt_verification'
        else:
            show_text_dialog("OPT Verification", "Данный адрес эл. почты не зарегистрирован")





















class OPTVerificationScreen(MDScreen):
    def __init__(self, **kw):
        super(OPTVerificationScreen, self).__init__(**kw)

        self.toolbar = MDTopAppBar(
            title = "OPT Verification",
            pos_hint = {"top": 1},
            left_action_items=[["arrow-left", lambda x: self.back()]]
        )
        self.add_widget(self.toolbar)

        self.code_input = MDTextField(
            hint_text = "Код из письма",
            size_hint = (.5, .1),
            pos_hint = {'center_x': .5, 'y': .5},
            mode = "rectangle"
        )
        self.add_widget(self.code_input)

        self.send_btn = MDIconButton(
            icon = "send-outline",
            theme_icon_color = "Custom",
            icon_color = Color.Primary,
            pos_hint = {'center_x': .8, 'y': .5}
        )
        self.send_btn.bind(on_release = self.send_btn_click)
        self.add_widget(self.send_btn)

    def send_btn_click(self, instance):
        self.manager.current = 'new_password'

    def back(self):
        self.manager.current = 'forgot_password'



















class NewPasswordScreen(MDScreen):
    def __init__(self, **kw):
        super(NewPasswordScreen, self).__init__(**kw)

        self.toolbar = MDTopAppBar(
            title = "New Password",
            pos_hint = {"top": 1},
            left_action_items=[["arrow-left", lambda x: self.back()]]
        )
        self.add_widget(self.toolbar)

        self.password_input = MDTextField(
            hint_text = 'Новый пароль',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.4},
            #foreground_color = (0, 0, 0, 255),
            error_color = (255, 0, 0),
            mode = 'rectangle'
        )
        self.password_input.bind(text = self.check_password_repeat)
        self.add_widget(self.password_input)
        
        self.password_confirm_input = MDTextField(
            hint_text = 'Подтверждение нового пароля',
            #font_size = 24,
            size_hint = (.9, .1),
            pos_hint = {'center_x': 0.5, 'y': 0.25},
            #foreground_color = (0, 0, 0, 255),
            error_color = (255, 0, 0),
            mode = 'rectangle'
        )
        self.password_confirm_input.bind(text = self.check_password_repeat)
        self.add_widget(self.password_confirm_input)

        self.change_btn = MDRaisedButton(
            text = 'Установить новый пароль',
            md_bg_color = Color.Primary,
            size_hint = (.5, .12),
            pos_hint = {'center_x': 0.5, 'y': 0.08}
        )
        self.change_btn.bind(on_release = self.change_btn_click)
        self.add_widget(self.change_btn)

    def change_btn_click(self, instance):
        pass

    def check_password_repeat(self, instance, password):
        print('password = ' + password)

        if self.password_confirm_input.text == self.password_input.text:
            self.password_confirm_input.error = False
        else:
            self.password_confirm_input.error = True

    def back(self):
        self.manager.current = 'forgot_password'




















class PrivacyScreen(MDScreen):
    def __init__(self, **kw):
        super(PrivacyScreen, self).__init__(**kw)

        privacy_text = str()
        with open('./privacy.ini', 'r') as file:
            privacy_text = file.read()

        # privacy_text = "Hello\nWorld"

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


















class MobileApp(MDApp):
    
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

        sm = MDScreenManager(transition = FadeTransition())
        sm.add_widget(LoginScreen(name = 'login'))
        sm.add_widget(RegScreen(name = 'reg'))
        sm.add_widget(HomeScreen(name = 'home'))
        sm.add_widget(PrivacyScreen(name = 'privacy'))
        sm.add_widget(ForgotPasswordScreen(name = 'forgot_password'))
        sm.add_widget(OPTVerificationScreen(name = 'opt_verification'))
        sm.add_widget(NewPasswordScreen(name = 'new_password'))
        return sm





def show_text_dialog(title_, text_):
    dialog = MDDialog(
        title = title_,
        text = text_
    )
    dialog.open()










if __name__ == '__main__':
    MobileApp().run()