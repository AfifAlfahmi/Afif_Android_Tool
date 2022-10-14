
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget



Builder.load_file("kivy_layouts/patch.kv")

class Patch(Widget):
    apk_path_et = ObjectProperty(None)

    pass