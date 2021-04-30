import flask
import json
import os,sys
import csv

from flask import Flask, render_template, jsonify, request, redirect, url_for
from rawls.rawls import Rawls
from rawls.utils import create_CSV, create_CSV_zone
from PIL import Image

from MONarchy.MONarchy import MONarchy
from MONarchy.Analyse import Analyse

app = flask.Flask(__name__)

def csv_footer(name_scene,tab,CSV_file,nb_samples,x,y,x2=None,y2=None):
    """
    remove the csv file and generate statistiques of this file
    """
    os.remove(CSV_file)
    if((x2 != None) and (y2 != None)):
        coordinate = "("+str(x)+","+str(y)+") to ("+str(x2)+","+str(y2)+")"
    else :
        coordinate = "("+str(x)+","+str(y)+")"
    analyse = Analyse(CSV_file)
    json_stat = analyse.infos()
    return render_template("stat_csv_image.html",
        name_scene = name_scene,
        coordinate = coordinate,
        nb_samples = nb_samples,
        json_stat = json_stat)

def save_png(name_scene):
    """
    save a png image from a rawls repertory
    """
    if not os.path.exists("static/images/" + name_scene + ".png"):
        for f in os.listdir(folder_rawls_path + "/" + name_scene):
            first_file = f
            break
        rawls_img = Rawls.load(folder_rawls_path + "/" + name_scene + "/" + first_file)
        rawls_img.save("static/images/" + name_scene + ".png")

def resize_image(name_scene):
    """
    save a png image with size (300,300) from a rawls repertory for display in website
    """
    save_png(name_scene)
    im = Image.open("static/images/" + name_scene + ".png")
    original_image_width,original_image_height = im.size
    size = (300,300)
    im.thumbnail(size)
    im.save("static/images/" + name_scene + "_300.png")
    img_resize = "images/" + name_scene + "_300.png"
    res = [img_resize,original_image_width,original_image_height]
    return res

def pixel_CSV_stat_header(name_scene=None, x=0, y=0, nb_samples=-1):
    """
    create a csv file from a rawls repertory by indicating the pixel to study
    """
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    create_CSV(folder_rawls_path + "/" + name_scene,x,y,folder_rawls_path,nb_samples)
    if nb_samples == -1:
        nb_samples = 0
        for name in os.listdir(folder_rawls_path + "/" + name_scene):
            if name.endswith(".rawls"):
                nb_samples += 1
    CSV_file = folder_rawls_path + "/" + name_scene + "_" + str(x) + "_" + str(y) + ".csv"
    res = [CSV_file,nb_samples]
    return res

@app.route("/up")  
def up():
    """
    Just for test if API is up

    Returns :
    {string} -- ok if API is up
    """
    return "ok"

@app.route("/home")
@app.route("/")
def home():
    """
    
    """
    img = request.args.get('img')
    xCoordinate = request.args.get('X-coordinate')
    yCoordinate = request.args.get('Y-coordinate')
    if img in scene_list:
        li = resize_image(img)
        link_img = li[0]
        original_image_width = li[1]
        original_image_height = li[2]
        if((xCoordinate != None)and(yCoordinate != None)):
            xCoordinate = int(xCoordinate)
            yCoordinate = int(yCoordinate)
            li = pixel_CSV_stat_header(img,xCoordinate,yCoordinate)
            nb_samples = li[1]
            coordinate = "("+str(xCoordinate)+","+str(yCoordinate)+")"
            analyse = Analyse(li[0])
            json_stat = analyse.infos()
            os.remove(li[0])
            return render_template("home.html",scenes = scene_list,image_ref = img, image = link_img,
                original_image_width = original_image_width,original_image_height = original_image_height,
                xCoordinate = xCoordinate,
                yCoordinate = yCoordinate,
                coordinate = coordinate,
                nb_samples = nb_samples,
                json_stat = json_stat)
        return render_template("home.html",scenes = scene_list,image_ref = img, image = link_img,
            original_image_width = original_image_width,
            original_image_height = original_image_height,
            xCoordinate = xCoordinate,
            yCoordinate = yCoordinate)
    return render_template("home.html",scenes = scene_list, image_ref = img,xCoordinate = xCoordinate,
        yCoordinate = yCoordinate)

@app.route("/list")
def list():
    """
    display a list of the rawls scene
    """
    format = request.args.get('format')
    if format == "json":
        return redirect(url_for('json_list'))
    return render_template("list.html",scenes = scene_list)

@app.route("/json_list")
def json_list():
    """
    display a list of the rawls scene in json
    """
    rawls_folders = {"rawls_folders" : scene_list}
    return jsonify(rawls_folders)

@app.route("/<name_scene>/png/ref")
def png(name_scene=None):
    """"
    display a png image from the rawls repertory
    """
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    save_png(name_scene)
    return render_template("png_image.html",name_scene = name_scene, image_png = "images/"+name_scene+".png")

@app.route("/<name_scene>/<int:x>/<int:y>")
@app.route("/<name_scene>/<int:x>/<int:y>/<int:nb_samples>")
def pixel_CSV_stat(name_scene=None, x=0, y=0, nb_samples=-1):
    """
    returns the statistics in json of the rawls directory indicating the pixel to study
    """
    li = pixel_CSV_stat_header(name_scene, x, y, nb_samples)
    CSV_file = li[0]
    nb_samples = li[1]
    analyse = Analyse(CSV_file)
    json_stat = analyse.infos()
    os.remove(CSV_file)
    return jsonify(json_stat)

@app.route("/<name_scene>/<int:x1>-<int:x2>/<int:y1>-<int:y2>")
@app.route("/<name_scene>/<int:x1>-<int:x2>/<int:y1>-<int:y2>/<int:nb_samples>")
def area_CSV_stat(name_scene=None, x1=0, y1=0,x2=1,y2=0, nb_samples=-1):
    """
    returns the statistics in json of the rawls directory indicating the area of the pixels to study
    """
    pwd = os.getcwd()
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    print("out : ",folder_rawls_path)
    create_CSV_zone(folder_rawls_path + "/" + name_scene,x1,y1,x2,y2,folder_rawls_path,nb_samples)

    os.chdir(pwd)
    if nb_samples == -1:
        nb_samples = 0
        for name in os.listdir(folder_rawls_path + "/" + name_scene):
            if name.endswith(".rawls"):
                nb_samples += 1
    CSV_file = folder_rawls_path + "/" + name_scene + "_" + str(x1) + "_" + str(y1) + "_to_" + str(x2) + "_" + str(y2) + ".csv"
    analyse = Analyse(CSV_file)
    json_stat = analyse.infos()
    os.remove(CSV_file)
    return jsonify(json_stat)

if __name__ == "__main__":
    with open('./config.json', 'r') as f:
        config = json.load(f)
    folder_rawls_path = config['path']
    scene_list = [ f for f in os.listdir(folder_rawls_path) if os.path.isdir(os.path.join(folder_rawls_path,f)) ]
    errors = ["ERROR : Your name of the scene doesn't exist"]
    app.run(debug=True)