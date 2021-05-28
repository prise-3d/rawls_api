from flask.templating import render_template
from .api import app
from flask_testing import TestCase

import os
import tempfile,json

import pytest
import click

class MyTest(TestCase):
    
    def create_app(self):
        app.testing = True
        return app

    def test_up(self):
        response = self.client.get('/up')
        self.assertEqual(response.json, "ok")
        response = self.client.get('/up?img=test')
        self.assertEqual(response.json, "yes")
    
    def test_list(self):
        response = self.client.get('/list')
        self.assertEqual(response.json, dict({'rawls_folders': ['p3d_villa-lights-on', 'p3d_bidir']}))
    
    def test_pixel_CSV_stat(self):
        response = self.client.get('/p3d_bidir/0/0/15')
        d = '[["0_0_R", {"mean": 0.17115751991333333, "median": 0.14318848, "MoN": 0.1676086442, "GMoN": 0.137377932, "Bin_GMoN": 0.137377932, "Bayesian MoN": 0.17009565652996017}], ["0_0_G", {"mean": 0.161770725376, "median": 0.11468506, "MoN": 0.1698059088, "GMoN": 0.1306213372, "Bin_GMoN": 0.1306213372, "Bayesian MoN": 0.16069889680981372}], ["0_0_B", {"mean": 0.15110545183733332, "median": 0.0848999, "MoN": 0.106566475712, "GMoN": 0.09157453221428571, "Bin_GMoN": 0.09157453221428571, "Bayesian MoN": 0.14827132405751814}]]'
        self.assertEqual(response.json, d)

    def test_png(self):
        response = self.client.get('p3d_bidir/png/ref')
        self.assertEqual(response.json, dict({"image_path": "./static/images/p3d_bidir.png"}))

    def test_home(self):
        response = self.client.get('/')
        d = {
            "name_scene": None, 
            "scenes": [
                "p3d_villa-lights-on", 
                "p3d_bidir"
            ], 
            "xCoordinate": None, 
            "yCoordinate": None
        }
        self.assertEqual(response.json, d)
        response = self.client.get('/home')
        self.assertEqual(response.json, d)

        response = self.client.get('/home?name_scene=p3d_bidir')
        d = {
            "image": "images/p3d_bidir_300.png", 
            "name_scene": "p3d_bidir", 
            "original_image_height": 80, 
            "original_image_width": 80, 
            "scenes": [
                "p3d_villa-lights-on", 
                "p3d_bidir"
            ], 
            "xCoordinate": None, 
            "yCoordinate": None
        }
        self.assertEqual(response.json, d)

        response = self.client.get('/home?name_scene=p3d_bidir&X-coordinate=0&Y-coordinate=0')
        d = {
            "image": "images/p3d_bidir_300.png", 
            "json_stat": "[[\"0_0_R\", {\"mean\": 0.181697607935, \"median\": 0.180541995, \"MoN\": 0.16141619157142856, \"GMoN\": 0.1910502133333333, \"Bin_GMoN\": 0.1910502133333333, \"Bayesian MoN\": 0.18109119623432862}], [\"0_0_G\", {\"mean\": 0.176372600032, \"median\": 0.16268921, \"MoN\": 0.14777047199999999, \"GMoN\": 0.19320678833333335, \"Bin_GMoN\": 0.19320678833333335, \"Bayesian MoN\": 0.17556696449615827}], [\"0_0_B\", {\"mean\": 0.193677292678, \"median\": 0.0903625475, \"MoN\": 0.1590292812857143, \"GMoN\": 0.163225864456, \"Bin_GMoN\": 0.163225864456, \"Bayesian MoN\": 0.18996608283593455}]]", 
            "name_scene": "p3d_bidir", 
            "nb_samples": 20, 
            "original_image_height": 80, 
            "original_image_width": 80, 
            "scenes": [
                "p3d_villa-lights-on", 
                "p3d_bidir"
            ], 
            "xCoordinate": 0, 
            "yCoordinate": 0
        }
        self.assertEqual(response.json, d)

        response = self.client.get('/home?name_scene=p3d_bidir&X-coordinate=0&Y-coordinate=0&nb_samples=19')
        d = {
            "image": "images/p3d_bidir_300.png", 
            "json_stat": "[[\"0_0_R\", {\"mean\": 0.19126063993157896, \"median\": 0.21789551, \"MoN\": 0.16445414349999998, \"GMoN\": 0.20413716599999998, \"Bin_GMoN\": 0.20413716599999998, \"Bayesian MoN\": 0.19078142925782926}], [\"0_0_G\", {\"mean\": 0.18565536845473685, \"median\": 0.21069336, \"MoN\": 0.15328470733333333, \"GMoN\": 0.20374552499999998, \"Bin_GMoN\": 0.20374552499999998, \"Bayesian MoN\": 0.18497554641234418}], [\"0_0_B\", {\"mean\": 0.20387083439789475, \"median\": 0.095825195, \"MoN\": 0.1695632956666667, \"GMoN\": 0.167312167856, \"Bin_GMoN\": 0.167312167856, \"Bayesian MoN\": 0.20015346009496443}]]", 
            "name_scene": "p3d_bidir", 
            "nb_samples": 19, 
            "original_image_height": 80, 
            "original_image_width": 80, 
            "scenes": [
                "p3d_villa-lights-on", 
                "p3d_bidir"
            ], 
            "xCoordinate": 0, 
            "yCoordinate": 0
        }
        self.assertEqual(response.json, d)