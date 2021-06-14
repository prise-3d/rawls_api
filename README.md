# rawls_api
REST-API for Rawls consultation

# how to start API
First

You must modif/create a json file which calls config.json where it contains the path of rawls repertories with the title of the datum "path" and the path of image repertories with a title of the datum "images_path".

For example :

    {
	    "path":"./static/rawls",
	    "images_path":"./static/images"
    }

Second

Go to the location of the API in your command prompt. Install all the necessary modules with the command:

    pip3 install -r requierement.txt

Finally, to launch the API, do the following command:

    pip3 api.py

If you want to learn more about the route of API check out the wiki at https://github.com/prise-3d/rawls_api/wiki