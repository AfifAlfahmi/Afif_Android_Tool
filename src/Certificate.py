
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget

from scripts.signer_script import signer_script

Builder.load_file("kivy_layouts/certificate.kv")

class Certificate(Widget):
    outKeyFile = ObjectProperty(None)
    c_name = ObjectProperty(None)
    org = ObjectProperty(None)

    loc = ObjectProperty(None)
    country = ObjectProperty(None)
    keyPass = ObjectProperty(None)
    storePass = ObjectProperty(None)
    alias = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Certificate, self).__init__(**kwargs)
        self.createCertBtn = self.ids.creCertBtn
        self.cert_res_status = self.ids.cert_res_status

        self.createCertBtn.bind(on_press=lambda z: self.createCertificate())



    def createCertificate(self):
        outKeyFile =  self.outKeyFile.text+".jks"
        c_name = self.c_name.text
        org = self.org.text

        loc = self.loc.text
        country = self.country.text
        keyPass = self.keyPass.text
        storePass =self.storePass.text
        alias = self.alias.text


        if(alias.count(" ") > 0) or outKeyFile.count(" ") > 0:
            print(f"found space in the input ")
            self.cert_res_status.text = "space not allowed"

        elif(not outKeyFile or not c_name or not org or not loc or not country or not keyPass or not storePass or not alias):
            print(f"found empty field ")
            self.cert_res_status.text = "all the fields required"


        else:
          createCertRes = signer_script.generateCert(outKeyFile, c_name, "dkkfg", org, loc,country, keyPass,
                     storePass, alias)
          self.cert_res_status.text = createCertRes

    pass