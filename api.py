# main import
import flask
import json
import csv
import os,sys

# modules import
from PIL import Image
from flask import Flask, render_template, jsonify, request, redirect, url_for
from MONarchy.MONarchy import MONarchy
from MONarchy.Analyse import Analyse
from rawls.rawls import Rawls
from rawls.utils import create_CSV, create_CSV_zone


app = flask.Flask(__name__) 
errors = ["ERROR : Your name of the scene doesn't exist",
"ERROR : coordinate too high, please enter a correct coordinate",
"ERROR : coordinate too low, please enter a correct coordinate",
"ERROR : not a correct argument",
"ERROR : method of the request (GET/POST) doesn't good"]
with open('./config.json', 'r') as f:
    config = json.load(f)
    folder_rawls_path = config['path']
    scene_list = [ f for f in os.listdir(folder_rawls_path) if os.path.isdir(os.path.join(folder_rawls_path,f)) ]
  
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

def pixel_CSV_stat_header(name_scene, x, y, nb_samples=-1):
    """
    create a csv file from a rawls repertory by indicating the pixel to study
    """
    if name_scene not in scene_list:
        return errors[0]
    # save_png(name_scene)
    # im = Image.open("static/images/" + name_scene + ".png")
    # original_image_width,original_image_height = im.size
    # if (original_image_width < x) or (original_image_height < y):
    #     return errors[1]
    if (x < 0) or (y < 0):
        return errors[2]
    create_CSV(folder_rawls_path + "/" + name_scene,x,y,"/tmp",nb_samples)
    if nb_samples == -1:
        nb_samples = 0
        for name in os.listdir(folder_rawls_path + "/" + name_scene):
            if name.endswith(".rawls"):
                nb_samples += 1
    CSV_file = "/tmp/" + name_scene + "_" + str(x) + "_" + str(y) + ".csv"
    res = [CSV_file,nb_samples]
    return res

def list_pixel_stat_header(name_scene,list_pix):
    """
    return json stat of the list of the pixels
    """
    res = []
    for coordinate in list_pix:
        li = pixel_CSV_stat_header(name_scene,coordinate[0],coordinate[1])
        CSV_file = li[0]
        analyse = Analyse(CSV_file)
        json_stat = analyse.infos()
        os.remove(CSV_file)
        res.append(json_stat)
    
    return res

@app.route("/up")  
def up():
    """
    Just for test if API is up

    Returns :
    {string} -- ok if API is up
    """
    img = request.args.get('img')
    if img != None:
        return "yes"
    return "ok"

@app.route("/home")
@app.route("/")
def home():
    """
    home page regroupe all functions in one interface
    ---
    get:
        description: get a statistiques of the pixel of the rawls scene, display a png image, choose a scene to study.
        parameters:
            - name: name_scene
                in: arguments
                description: name of the scene to study
                type: string
                required: false
            - name: X-coordinate
                in: arguments
                description: horizontal coordinate of the pixel to study
                type: integer
                required: false
            - name: Y-coodinate
                in: arguments
                description: vertical coordinate of the pixel to study
                type: integer
                required: false
        responses:
            200:
                description:
                    -return a home page with arguments:
                        -scenes: {[string]} list of name of the scenes
                        -name_scene: {string} name of the scene to study
                        -image: {string} path of the png resize image
                        -original_image_width: {int} width of the png image of the scene
                        -original_image_height: {int} height of the png image of the scene
                        -xCoordinate: {int} horizontal coordinate of the pixel to study
                        -yCoordinate: {int} vertical coordinate of the pixel to study
                        -nb_samples: {int} number of the samples we will use for the statistiques
                        -json_stat: a json object with statistiques of the pixel study
                    -return a home page with arguments:
                        -scenes: {[string]} list of name of the scenes
                        -name_scene: {string} name of the scene to study
                        -image: {string} path of the png resize image
                        -original_image_width: {int} width of the png image of the scene
                        -original_image_height: {int} height of the png image of the scene
                        -xCoordinate: {int} horizontal coordinate of the pixel to study
                        -yCoordinate: {int} vertical coordinate of the pixel to study
                    -return a home page with arguments:
                        -scenes: {[string]} list of name of the scenes
                        -name_scene: {string} name of the scene to study
                        -xCoordinate: {int} horizontal coordinate of the pixel to study
                        -yCoordinate: {int} vertical coordinate of the pixel to study
                    -return a error page if coordinate is not valid with argument :
                        - {string} error : a sentence of the error
            404:
                description:
                    -name of scene not found.
            500:
                description:
                    -we don't use X-coordinate and/or Y-coordinate and/or nb_samples as an integer
    """
    name_scene = request.args.get('name_scene')
    xCoordinate = request.args.get('X-coordinate')
    yCoordinate = request.args.get('Y-coordinate')
    nb_samples = request.args.get('nb_samples')
    if name_scene in scene_list:
        li = resize_image(name_scene)
        link_img = li[0]
        original_image_width = li[1]
        original_image_height = li[2]
        if((xCoordinate != None)and(yCoordinate != None)):
            xCoordinate = int(xCoordinate)
            yCoordinate = int(yCoordinate)
            if(nb_samples == None):
                nb_samples = -1
            nb_samples = int(nb_samples)
            li = pixel_CSV_stat_header(name_scene,xCoordinate,yCoordinate,nb_samples)
            if isinstance(li,str):
                return render_template("error.html", error = li)
            nb_samples = li[1]
            analyse = Analyse(li[0])
            json_stat = analyse.infos()
            os.remove(li[0])
            return render_template("home.html",
                scenes = scene_list,
                name_scene = name_scene,
                image = link_img,
                original_image_width = original_image_width,
                original_image_height = original_image_height,
                xCoordinate = xCoordinate,
                yCoordinate = yCoordinate,
                nb_samples = nb_samples,
                json_stat = json_stat)
        return render_template("home.html",
            scenes = scene_list,
            name_scene = name_scene,
            image = link_img,
            original_image_width = original_image_width,
            original_image_height = original_image_height,
            xCoordinate = xCoordinate,
            yCoordinate = yCoordinate)
    return render_template("home.html",
        scenes = scene_list,
        name_scene = name_scene,
        xCoordinate = xCoordinate,
        yCoordinate = yCoordinate)

@app.route("/list")
def list():
    """
    display a list of the rawls scene.
    ---
    get:
        description: Get a list of rawls scene.
        parameters:
            - name: format
                in: parametres
                description: format output (json)
                type: string
                required: false
        responses:
            200:
                description: 
                    -list page to be returned with argument :
                        -scenes : {[string]} list of scenes
            302:
                description:
                    -if format = json, redirect url to '/json_list'
    """
    format = request.args.get('format')
    if format == "json":
        return redirect(url_for('json_list'))
    return render_template("list.html",scenes = scene_list)

@app.route("/json_list")
def json_list():
    """
    display a list of the rawls scene in json.
    ---
    get:
        description: Get a list of the scenes in format json.
        
        responses:
            200:
                description: json object to be returned.
    """
    rawls_folders = {"rawls_folders" : scene_list}
    return jsonify(rawls_folders)

@app.route("/<name_scene>/png/ref")
def png(name_scene=None):
    """"
    display a png image from the rawls repertory
    ---
    get:
        description: Get a single foo with the bar ID.
        parameters:
            - name: name_scene
                in: path
                description: name of the scene to study
                type: string
                required: true
        responses:
            200:
                description: 
                    -return a png_image page with arguments :
                        -name_scene: {string} name of the scene
                        -image_png: {string} path of the png image
                    -return a error page if coordinate is not valid with argument :
                        - {string} error : a sentence of the error
    """
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    save_png(name_scene)
    return render_template("png_image.html",name_scene = name_scene, image_png = "images/"+name_scene+".png")

@app.route("/<name_scene>/<int:x>/<int:y>")
@app.route("/<name_scene>/<int:x>/<int:y>/<int:nb_samples>")
def pixel_CSV_stat(name_scene, x, y, nb_samples=50):
    """
    returns the statistics in json of the rawls directory indicating the pixel to study.
    ---
    get:
        description: get a statistiques of the pixel of the rawls scene.
        parameters:
            - name: name_scene
                in: path
                description: name of the scene to study
                type: string
                required: true
            - name: x
                in: path
                description: horizontal coordinate of the pixel to study
                type: integer
                required: true
            - name: y
                in: path
                description: vertical coordinate of the pixel to study
                type: integer
                required: true
            - name: nb_samples
                in: path
                description: number of the samples we will use for the statistiques
                type: integer
                default: -1 (all samples in rawls repertory)
                required: false
        responses:
            200:
                description:
                    -return a json object with statistiques of the pixel study
                    -return a error page if coordinate is not valid with argument :
                        - {string} error : a sentence of the error
            500:
                description: 
                    -name of scene not found.
                    -Exception: Unvalid number for a samples
    """
    li = pixel_CSV_stat_header(name_scene, x, y, nb_samples)
    if isinstance(li,str):
        return render_template("error.html", error = li)
    CSV_file = li[0]
    nb_samples = li[1]
    analyse = Analyse(CSV_file)
    json_stat = analyse.infos()
    os.remove(CSV_file)
    return jsonify(json_stat)

@app.route("/<name_scene>")
def list_pixel_stat(name_scene, methods = ['POST']):
    """
    returns the statistics in json of the rawls directory indicating a list of the pixels to study
    ---
    post:
        description: get a statistiques of the list of pixels indicated of the rawls scene.
        parameters:
            - name: name_scene
                in: path
                description: name of the scene to study
                type: string
                required: true
            - json_file
                in: parametres
                description: json which contains a list of pixel
                type: json
                required: true
                example : 
                    {
                        "pixels": [[8,4],[1,2]]
                    }
        responses:
            200:
                description:
                    -return a json object with statistiques of the list of the pixels study
            405:
                description:
                    -method not allowed
            500:
                description: 
                    -name of scene not found.
    """
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    if request.method == 'POST':
        request_data = request.get_json()
        if request_data:
            if 'pixels' in request_data:
                if (type(request_data['pixels']) == list) and (len(request_data['pixels']) > 0):
                    json_stat = list_pixel_stat_header(name_scene,request_data['pixels'])
                    return jsonify(json_stat)
            return render_template("error.html", error = errors[3])
    return render_template("error.html", error = errors[4])

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')