
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget





Builder.load_file("../kivy_layouts/sign_layout.kv")

class Sign(Widget):
    keyPathET = ObjectProperty(None)
    apk_path_et = ObjectProperty(None)
    signStorePass: ObjectProperty(None)
    signAlias: ObjectProperty(None)
    signKeyPass: ObjectProperty(None)
    pass