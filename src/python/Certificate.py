
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget


class Certificate(Widget):
    outKeyFile = ObjectProperty(None)
    c_name = ObjectProperty(None)
    org = ObjectProperty(None)

    loc = ObjectProperty(None)
    country = ObjectProperty(None)
    keyPass = ObjectProperty(None)
    storePass = ObjectProperty(None)
    alias = ObjectProperty(None)

    pass