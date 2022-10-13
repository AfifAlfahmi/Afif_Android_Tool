# Afif Android Tool

Afif Android Tool is a tool for signing, patching, and analyzing Android Apps, it is developed using python



# Features

* Sign Apk files
* Log the names of the classes & functions 
* Detect unsafe activities and receivers with the ability to launch it
* Extract the APKs files that are installed on the device
* Upload files to Android device in a quick & easy way


# Installation


<code> git clone https://github.com/AfifAlfahmi/Afif_Android_Tool.git </code>

<code>cd Afif_Android_Tool</code>
<br>



 <hr>

### Optional

It’s recommended to create a new virtual environment to separates the dependencies of different projects
 
<code>python3 -m pip install --upgrade pip setuptools virtualenv </code>

<code>python3 -m virtualenv afif_venv</code>


activate the virtual environment

Windows <code>afif_venv\Scripts\activate</code>

Linux or Mac <code>source afif_venv/bin/activate</code>

 <hr>

### Required 

* python 3.6 or higher <br/><br/>

* install the required dependencies

&emsp; &ensp; &ensp; Windows <code>pip install -r win_requirements.txt</code>

&emsp; &ensp; &ensp; Mac &emsp; &ensp; <code>pip install -r mac_requirements.txt</code>

&emsp; &ensp; &ensp; Linux  &ensp; &ensp; <code>pip install -r linux_requirements.txt</code>



# Getting Started

<code>cd src </code>

<code>python afif_android_tool.py  </code>

<br/><br/>