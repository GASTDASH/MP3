import io
import sqlite3
from supabase import create_client, Client
from plyer import notification
import sys

from kivy.app import App
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.loader import Loader

from kivy.properties import StringProperty, ColorProperty, BooleanProperty

from kivymd.uix.gridlayout import MDGridLayout

from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import *
from kivymd.uix.transition import *

from kivymd.uix.label import MDLabel

from kivymd.uix.scrollview import MDScrollView

from kivymd.uix.card import MDCard

from kivymd.uix.toolbar import MDTopAppBar

from kivymd.uix.bottomnavigation import *

from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog


account_id = None # Logged In Account ID
balance = float(0) # Logged In Account balance
dark_mode = False # Dark Mode

# SQLite Connection
conn = sqlite3.connect('tunec.db')
cur = conn.cursor()

# Supabase Connection
url: str = "https://yuomdsktqooaxwfhvhfn.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1b21kc2t0cW9vYXh3Zmh2aGZuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzc1ODYyMCwiZXhwIjoyMDIzMzM0NjIwfQ.kRfxxaHZ_CBjjZ4yC4LULjV5J5ROybQf1Jz0Hq4z1eI"
try:
    supabase: Client = create_client(url, key)
    test = supabase.table("accounts").select("*").execute()
except:
    print(f"\n\n\n\nПИЗДА РУЛЮ!!!! ИНЕТА НЕМА!!!!! НЕ МОГУ ПОДКЛЮЧИТЬСЯ!!!!!!!!!!!!!!")
    sys.exit()

#################
#   Карточка, использующаяся на экране Profile в качестве кнопок
#   12.02.2024
#   By GASTDASH
#################
class MYProfileCard(MDCard):
    text_title = StringProperty()
    text_subtitle = StringProperty()
    icon = StringProperty()
    icon_color = ColorProperty()

    def __init__(self, **kw):
        super(MYProfileCard, self).__init__(**kw)

#################
#   Карточка, использующаяся в качестве кнопок ТопБара
#   12.02.2024
#   By GASTDASH
#################
class MYTopBar(MDCard):
    title = StringProperty()
    back = BooleanProperty()

    def __init__(self, **kw):
        super(MYTopBar, self).__init__(**kw)

#################
#   Карточка, использующаяся в качестве текстового поля поиска
#   12.02.2024
#   By GASTDASH
#################
class MYSearchTextField(MDCard):
    hint_text = StringProperty()

    def __init__(self, **kw):
        super(MYSearchTextField, self).__init__(**kw)

#################
#   Карточка, использующаяся в качестве кнопок выбора сервиса
#   12.02.2024
#   By GASTDASH
#   
#   touch_down, touch_up - функции для изменения цветов карточки при нажатии и отжатии
#################
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

#################
#   Экран Login
#   12.02.2024
#   By GASTDASH
#################
class LoginScreen(MDScreen):
    def __init__(self, **kw):
        super(LoginScreen, self).__init__(**kw)
        
    def login_btn_click(self, *args):
        response = supabase.table('accounts').select("*").eq('username', f"{self.ids.username_input.text}").eq('password', f"{self.ids.password_input.text}").execute().data
        print("\n\n\n[G_DEBUG --> Supabase] response")
        print(response)

        response_email = supabase.table('accounts').select("*").eq('email', f"{self.ids.username_input.text}").eq('password', f"{self.ids.password_input.text}").execute().data
        print("\n\n\n[G_DEBUG --> Supabase] response_email")
        print(response_email)

        if (len(response_email) > 0):
            response = response_email

        print("\n\n[G_DEBUG] response")
        print(response)

        if (len(response) > 0 or len(response_email) > 0):
            print(bcolors.BOLD + bcolors.OKGREEN + '\n\n[G_DEBUG] Authorization successful!' + bcolors.ENDC)

            global account_id
            account_id = response[0]["account_id"]
            print(f"\n\n[G_DEBUG] account_id = {account_id}")

            HomeScreen.update_balance(HomeScreen(), args)
            print(f"\n\n[G_DEBUG] balance = {balance}")

            self.ids.username_input.text = ''
            self.ids.password_input.text = ''

            result = supabase.table("accounts").select("username").eq("account_id", f"{account_id}").execute().data
            if result is not None:
                MobileApp.username = result[0]["username"]
            self.manager.get_screen("home").on_open(self.manager.get_screen("home"))
            self.manager.current = 'home'
        else:
            show_text_dialog('Авторизация', 'Неправильный логин или пароль')

    def registration_btn_click(self, instance):
        self.manager.current = 'reg'

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
        # notification.notify('Some title', 'Some message text').notify('Some title', 'Some message text')

#################
#   Экран Registration
#   12.02.2024
#   By GASTDASH
#################
class RegScreen(MDScreen):
    def __init__(self, **kw):
        super(RegScreen, self).__init__(**kw)

        self.email_error = False
        
        response = supabase.table('accounts').select("email").execute()
        print("\n\n\n[G_DEBUG --> Supabase]")
        print(response.data)

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
            print('\n\n[G_DEBUG] Registration successful!')

            account = (
                self.ids.username_input.text,
                self.ids.email_input.text,
                self.ids.password_input.text
            )

            response = supabase.table("accounts").insert({"username": account[0], "email": account[1], "password": account[2], "balance": 0.0})

            show_text_dialog('Регистрация', f'Пользователь {self.ids.username_input.text} был успешно зарегестрирован в системе')
            
            self.ids.username_input.text = ''
            self.ids.email_input.text = ''
            self.ids.password_input.text = ''
            self.ids.password_confirm_input.text = ''
            
            self.email_error = False

            self.manager.current = 'login'

    def check_email(self, email):
        print('\n\n[G_DEBUG] email = ' + email)

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
        print('\n\n[G_DEBUG] password = ' + password)

        if self.password_confirm_input.text == self.password_input.text:
            self.password_confirm_input.error = False
        else:
            self.password_confirm_input.error = True

#################
#   Экран Home
#   12.02.2024
#   By GASTDASH
#################
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
        response = supabase.table("accounts").select("avatar").eq("account_id", f"{account_id}").execute().data
        if response is not None:
            if response[0]["avatar"] is not None:
                avatar = response[0]["avatar"]
        else:
            avatar = './assets/avatar.png'
        self.ids.avatar_home.source = avatar
        self.ids.avatar_profile.source = avatar
    
    def update_username(self, *args):
        self.ids.home_username_label.text = f"Hello {MobileApp.username}"
        self.ids.profile_username_label.text = f"Hello {MobileApp.username}"

    def update_balance(self, *args):
        # cur.execute(f"SELECT balance FROM accounts WHERE account_id = \'{account_id}\'")
        # res = cur.fetchone()
        res = supabase.table("accounts").select("balance").eq("account_id", f"{account_id}").execute().data
        global balance
        if res is not None:
            if res[0]["balance"] is not None:
                balance = float(res[0]["balance"])
                self.balance = balance
        else:
            self.balance = -1
        
        print(f"\n\n[G_DEBUG] balance = {self.balance}")
        if self.hide_balance_bool:
            self.ids.balance_label.text = f"Ваш баланс: *****"
        else:
            self.ids.balance_label.text = f"Ваш баланс: [color={Color.Primary}][b]${str(self.balance)}[/b][/color]"

    def hide_balance(self, *args):
        self.hide_balance_bool = not self.hide_balance_bool

        self.update_balance(args)

    def dark_mode_switch(self, *args):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            MobileApp.colors = MobileApp.colors_dark
        else:
            self.theme_cls.theme_style = "Light"
            MobileApp.colors = MobileApp.colors_light
        print(f"\n\n[G_DEBUG] Now theme_cls.theme_style is {self.theme_cls.theme_style}")

    def logout(self, *args):
        self.ids.navigator.switch_tab("home")
        self.manager.current = "login"

#################
#   Экран Add Payment Method
#   12.02.2024
#   By GASTDASH
#################
class AddPaymentMethodScreen(MDScreen):
    def __init__(self, **kw):
        super(AddPaymentMethodScreen, self).__init__(**kw)

        self.ids.topbar.ids.back_btn.bind(on_release = self.back)

    def back(self, *args):
        self.manager.current = 'home'

#################
#   Экран Forgot Password
#   12.02.2024
#   By GASTDASH
#################
class ForgotPasswordScreen(MDScreen):
    def __init__(self, **kw):
        super(ForgotPasswordScreen, self).__init__(**kw)

    def back(self, w, touch):
        if w.collide_point(*touch.pos):
            self.manager.current = 'login'
            

    def send_btn_click(self, instance):
        results = supabase.table("accounts").select("account_id").eq("email", f"{self.ids.email_input.text}").execute().data

        print('\n\n[G_DEBUG] \n', results)
        
        if len(results) > 0:
            global account_id
            account_id = results[0]["account_id"]
            print(f"\n\n[G_DEBUG] account_id = {account_id}")
            self.manager.current = 'opt_verification'
        else:
            show_text_dialog("OPT Verification", "Данный адрес эл. почты не зарегистрирован")

#################
#   Экран OPT Verification
#   12.02.2024
#   By GASTDASH
#################
class OPTVerificationScreen(MDScreen):
    def __init__(self, **kw):
        super(OPTVerificationScreen, self).__init__(**kw)

    def send_btn_click(self, instance):
        self.manager.current = 'new_password'

    def back(self):
        self.manager.current = 'forgot_password'

#################
#   Экран New Password
#   12.02.2024
#   By GASTDASH
#################
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
        print('\n\n[G_DEBUG] password = ' + self.ids.password_input.text)

        if self.ids.password_confirm_input.text == self.ids.password_input.text:
            self.ids.password_confirm_input.error = False
            return False
        else:
            self.ids.password_confirm_input.error = True
            return True

#################
#   Экран Privacy
#   12.02.2024
#   By GASTDASH
#################
class PrivacyScreen(MDScreen):
    def __init__(self, **kw):
        super(PrivacyScreen, self).__init__(**kw)

        with io.open('./privacy.ini', encoding='utf-8') as file:
            privacy_text = file.read()

        self.scrollview = MDScrollView(
            do_scroll_x = False,
            do_scroll_y = True,
            size_hint = (1, None),
            size = (Window.width, Window.height)
        )
        self.add_widget(self.scrollview)

        self.grid = MDGridLayout(
            size_hint = (1, None),
            cols = 1,
            padding = 20
        )
        self.grid.bind(minimum_height = self.grid.setter('height'))

        self.privacy_label = MDLabel(
            text = privacy_text,
            markup = True,
            size_hint = (1, None)
        )
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


# Цвета для терминала
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Цвета для виджетов
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


# Главный класс приложения
class MobileApp(MDApp):
    colors_light = {
        "Primary": "#0560fa",
        "Secondary": "#ec8000",
        "Success": "#35b369",
        "Warning": "#ebbc2e",
        "Info": "#2f80ed",
        "Error": "#ed3a3a",
        "Text1": "#141414",
        "Text2": "#3a3a3a",
        "Gray1": "#cfcfcf",
        "Gray2": "#a7a7a7"
    }
    colors_dark = {
        "Primary": "#ff0000",
        "Secondary": "#ec8000",
        "Success": "#35b369",
        "Warning": "#ebbc2e",
        "Info": "#2f80ed",
        "Error": "#ed3a3a",
        "Text1": "#141414",
        "Text2": "#3a3a3a",
        "Gray1": "#cfcfcf",
        "Gray2": "#a7a7a7"
    }
    colors = colors_light

    username = "{username}"   
    avatar_source = './assets/avatar.png'

    def build(self):
        Window.size = (360, 800)
        # Window.size = (1080, 2400)

        # Loader.loading_image = './assets/loading.gif'

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
        sm.add_widget(LoginScreen(name = 'login'))
        sm.add_widget(RegScreen(name = 'reg'))
        sm.add_widget(HomeScreen(name = 'home'))
        sm.add_widget(PrivacyScreen(name = 'privacy'))
        sm.add_widget(ForgotPasswordScreen(name = 'forgot_password'))
        sm.add_widget(OPTVerificationScreen(name = 'opt_verification'))
        sm.add_widget(NewPasswordScreen(name = 'new_password'))
        sm.add_widget(AddPaymentMethodScreen(name = 'add_payment_method'))
        return sm

# Отображение простого диалогового окна
def show_text_dialog(title_, text_):
    dialog = MDDialog(
        title = title_,
        text = text_
    )
    dialog.open()

if __name__ == '__main__':
    MobileApp().run()