from kivy.lang.builder import Builder
from kivymd.app import MDApp

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

    username = "{username}"   

    def build(self):
        return Builder.load_file('test.kv')
    
    def print_UN(self, *args):
        print(MobileApp.username)

    def change_UN(self, *args):
        MobileApp.username = "GASTDASH"

if __name__ == '__main__':
    MobileApp().run()