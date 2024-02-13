from kivy.lang.builder import Builder
from kivymd.app import MDApp
import hashlib
from kivy.loader import Loader

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

    avatar_source = "https://yuomdsktqooaxwfhvhfn.supabase.co/storage/v1/object/sign/avatars/lightny_sparky.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXJzL2xpZ2h0bnlfc3Bhcmt5LmpwZyIsImlhdCI6MTcwNzgwNDc5NywiZXhwIjozMTU1Mjc2MjY4Nzk3fQ.ZvlZBRTcFmX_G4rgQYciZL6jCLXlrnNKPGqexHVBla0&t=2024-02-13T06%3A13%3A17.475Z"

    def build(self):
        Loader.loading_image = './assets/loading.gif'

        return Builder.load_file('test.kv')
    
    def hash_sha512(self, text):
        return hashlib.sha512(bytes(text, 'utf-8')).hexdigest()

if __name__ == '__main__':
    MobileApp().run()