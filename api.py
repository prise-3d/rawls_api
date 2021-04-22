import flask
import json
import os,sys
import csv
import statistics

from flask import Flask, render_template, jsonify, request, redirect, url_for
sys.path.insert(0, os.path.abspath('../../rawls/rawls'))
from rawls.rawls import Rawls
from rawls.utils import create_CSV, create_CSV_zone

app = flask.Flask(__name__)

def stat_csv(tab):
    tab_R = []
    tab_G = []
    tab_B = []
    for i in range(len(tab[0])):
        tab_R.append(tab[i][0])
        tab_G.append(tab[i][1])
        tab_B.append(tab[i][2])
    mean_R = statistics.mean(tab_R)
    mean_G = statistics.mean(tab_G)
    mean_B = statistics.mean(tab_B)
    median_R = statistics.median(tab_R)
    median_G = statistics.median(tab_G)
    median_B = statistics.median(tab_B)
    median_high_R = statistics.median_high(tab_R)
    median_high_G = statistics.median_high(tab_G)
    median_high_B = statistics.median_high(tab_B)
    median_low_R = statistics.median_low(tab_R)
    median_low_G = statistics.median_low(tab_G)
    median_low_B = statistics.median_low(tab_B)
    return mean_R,mean_G, mean_B, median_R, median_G, median_B, median_high_R, median_high_G, median_high_B, median_low_R, median_low_G, median_low_B

def csv_footer(name_scene,tab,CSV_file,nb_samples,x,y,x2=None,y2=None):
    res = stat_csv(tab)
    os.remove(CSV_file)
    format = request.args.get('format')
    if((x2 != None) and (y2 != None)):
        coordinate = "("+str(x)+","+str(y)+") to ("+str(x2)+","+str(y2)+")"
    else :
        coordinate = "("+str(x)+","+str(y)+")"
    if format == "json":
        json_stat = {"name_scene" : name_scene,
        "coordinate" : coordinate,
        "nb_samples" : nb_samples,
        "mean_R" : res[0],
        "mean_G" : res[1],
        "mean_B" : res[2],
        "median_R" : res[3],
        "median_G" : res[4],
        "median_B" : res[5],
        "median_high_R" : res[6],
        "median_high_G" : res[7],
        "median_high_B" : res[8],
        "median_low_R" : res[9],
        "median_low_G" : res[10],
        "median_low_B" : res[11]}
        return jsonify(json_stat)
    return render_template("stat_csv_image.html",
        name_scene = name_scene,
        coordinate = coordinate,
        nb_samples = nb_samples,
        mean_R = res[0],
        mean_G = res[1],
        mean_B = res[2],
        median_R = res[3],
        median_G = res[4],
        median_B = res[5],
        median_high_R = res[6],
        median_high_G = res[7],
        median_high_B = res[8],
        median_low_R = res[9],
        median_low_G = res[10],
        median_low_B = res[11])

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/list")
def list():
    format = request.args.get('format')
    if format == "json":
        return redirect(url_for('json_list'))
    return render_template("list.html",scenes = scene_list)

@app.route("/json_list")
def json_list():
    rawls_folders = {"rawls_folders" : scene_list}
    return jsonify(rawls_folders)

@app.route("/<name_scene>/png/ref")
def png(name_scene=None):
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    if not os.path.exists("static/images/" + name_scene + ".png"):
        for f in os.listdir(folder_rawls_path + "/" + name_scene):
            first_file = f
            break
        rawls_img = Rawls.load(folder_rawls_path + "/" + name_scene + "/" + first_file)
        rawls_img.save("static/images/" + name_scene + ".png")
    return render_template("png_image.html",name_scene = name_scene, image_png = "images/"+name_scene+".png")

@app.route("/<name_scene>/<int:x>/<int:y>")
@app.route("/<name_scene>/<int:x>/<int:y>/<int:nb_samples>")
def pixel_CSV_stat(name_scene=None, x=0, y=0, nb_samples=-1):
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    # ici
    create_CSV(folder_rawls_path + "/" + name_scene,x,y,folder_rawls_path,nb_samples)
    if nb_samples == -1:
        nb_samples = 0
        for name in os.listdir(folder_rawls_path + "/" + name_scene):
            if name.endswith(".rawls"):
                nb_samples += 1
    CSV_file = folder_rawls_path + "/" + name_scene + "_" + str(x) + "_" + str(y) + ".csv"
    with open(CSV_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        tab = []
        for index,row in enumerate(spamreader):
            if index != 0:
                data1 = float(row[0])
                data2 = float(row[1])
                data3 = float(row[2])
                tab.append([data1,data2,data3])
    return csv_footer(name_scene,tab,CSV_file,nb_samples,x,y)

@app.route("/<name_scene>/<int:x1>-<int:x2>/<int:y1>-<int:y2>")
@app.route("/<name_scene>/<int:x1>-<int:x2>/<int:y1>-<int:y2>/<int:nb_samples>")
def area_CSV_stat(name_scene=None, x1=0, y1=0,x2=1,y2=0, nb_samples=-1):

    pwd = os.getcwd()
    if name_scene not in scene_list:
        return render_template("error.html", error = errors[0])
    create_CSV_zone(folder_rawls_path + "/" + name_scene,x1,y1,x2,y2,folder_rawls_path,nb_samples)
    os.chdir(pwd)
    if nb_samples == -1:
        nb_samples = 0
        for name in os.listdir(folder_rawls_path + "/" + name_scene):
            if name.endswith(".rawls"):
                nb_samples += 1
    CSV_file = folder_rawls_path + "/" + name_scene + "_" + str(x1) + "_" + str(y1) + "_to_" + str(x2) + "_" + str(y2) + ".csv"
    with open(CSV_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        tab = []
        for index,row in enumerate(spamreader):
            if index != 0:
                a,b,c = 0,1,2
                while(c<=((x2-x1+1)*(y2-y1+1)*3)):
                    data1 = float(row[a])
                    data2 = float(row[b])
                    data3 = float(row[c])
                    tab.append([data1,data2,data3])
                    a += 3
                    b += 3
                    c += 3
    return csv_footer(name_scene,tab,CSV_file,nb_samples,x1,y1,x2,y2)

if __name__ == "__main__":
    with open('./config.json', 'r') as f:
        config = json.load(f)
    folder_rawls_path = config['path']
    scene_list = [ f for f in os.listdir(folder_rawls_path) if os.path.isdir(os.path.join(folder_rawls_path,f)) ]
    errors = ["ERROR : Your name of the scene doesn't exist"]
    app.run(debug=True)