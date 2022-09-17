# Afif Android Tool

Afif Android Tool is a tool for signing, patching, and analyzing Android Apps, it is developed using python



# Features

* sign Apk files
* log the names of the classes & functions 
* detect unsafe activities and receivers with the ability to launch it
* Extract the APKs files that are installed on the device
* upload files to Android device in a quick & easy way


# Installation


<code> git clone https://github.com/AfifAlfahmi/Afif_Android_Tool.git </code>

<code>cd Afif_Android_Tool</code>
<br>



 <hr>

### Optional

It’s recommended to create a new virtual environment to separates the dependencies of different projects
 
<code>python -m pip install --upgrade pip setuptools virtualenv </code>

<code>python -m virtualenv afif_venv</code>


activate the virtual environment

windows 

<code>afif_venv\Scripts\activate</code>

linux or macOS

<code>source afif_venv/bin/activate</code>

 <hr>

### Required 


install the required dependencies

<code>pip install -r requirements.txt</code>

# Getting Started

<code>cd src </code>

<code>python afif_android_tool.py  </code>