# rawls_api
REST-API for Rawls consultation
You must modif a json file which calls config.json where it contains the path of rawls repertories with the title of the datum "path".  For example :
{
"path":"/home/theo/rawls/images"
}

Documentation of the route :
@app.route("/up")
    Just for test if API is up

    Returns :
    {string} -- ok if API is up
    
@app.route("/home")
@app.route("/")
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
   
@app.route("/list")

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

@app.route("/json_list")

    display a list of the rawls scene in json.
    ---
    get:
        description: Get a list of the scenes in format json.
        
        responses:
            200:
                description: json object to be returned.


@app.route("/<name_scene>/png/ref")

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

@app.route("/<name_scene>/<int:x>/<int:y>")
@app.route("/<name_scene>/<int:x>/<int:y>/<int:nb_samples>")

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

@app.route("/<name_scene>/<int:x1>-<int:x2>/<int:y1>-<int:y2>")
@app.route("/<name_scene>/<int:x1>-<int:x2>/<int:y1>-<int:y2>/<int:nb_samples>")

    returns the statistics in json of the rawls directory indicating the area of the pixels to study
    ---
    get:
        description: get a statistiques of the area indicated of the rawls scene.
        parameters:
            - name: name_scene
                in: path
                description: name of the scene to study
                type: string
                required: true
            - name: x1
                in: path
                description: horizontal coordinate of the top left corner of the area to study
                type: integer
                required: true
            - name: x2
                in: path
                description: horizontal coordinate of the bottom right corner of the area to study
                type: integer
                required: true
            - name: y1
                in: path
                description: vertical coordinate of the top left corner of the area to study
                type: integer
                required: true
            - name: y2
                in: path
                description: vertical coordinate of the bottom right of the area to study
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
                    -Invalid coodinate : if (x1,y1) is more right and/or bottom than (x2,y2)