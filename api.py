import flask
import json
import os

from rawls.rawls import Rawls
from flask import Flask, render_template

app = flask.Flask(__name__)

with open('./config.json', 'r') as f:
	config = json.load(f)
folder_rawls_path = config['path']
scene_list = [ f for f in os.listdir(folder_rawls_path) if os.path.isdir(os.path.join(folder_rawls_path,f)) ]
errors = ["ERROR : Your name of the scene doesn't exist"]

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/list")
def list():
    return render_template("list.html",scenes = scene_list)

@app.route("/<name_scene>/png/ref")
def png(name_scene=None):
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0]) #à faire
    if not os.path.exists("static/images/" + name_scene + ".png"):
        for f in os.listdir(folder_rawls_path + "/" + name_scene):
            first_file = f
            break
        rawls_img = Rawls.load(folder_rawls_path + "/" + name_scene + "/" + first_file)
        rawls_img.save("static/images/" + name_scene + ".png")
    return render_template("png_image.html",name_scene = name_scene, image_png = "images/"+name_scene+".png")

if __name__ == "__main__":
    app.run(debug=True)