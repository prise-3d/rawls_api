from flask.templating import render_template
from .api import app
from flask_testing import TestCase

import os
import tempfile,json

import pytest

class MyTest(TestCase):
    
    render_template = False
    
    def create_app(self):
        return app

    def test_up(self):
        # assert b'ok' in response.data
        response = self.client.get('/up')
        self.assert200(response)
        assert response.data == b"ok"
        response = self.client.get('/up?img=ioiao')
        self.assert200(response)
        assert b'yes' in response.data
   
    def test_list(self):
        response = self.client.get('/list')
        self.assert200(response)
        self.assert_template_used('list.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])

        response = self.client.get('/list?format=json')
        assert response.status_code == 302
        self.assertRedirects(response,'json_list')
    
    def test_json_list(self):
        response = self.client.get('/json_list')
        self.assertEqual(response.json, dict({'rawls_folders': ['p3d_villa-lights-on', 'p3d_bidir']}))
    
    def test_pixel_CSV_stat(self):
        response = self.client.get('/p3d_bidir/0/0')
        d = '[["0_0_R", {"mean": 0.181697607935, "median": 0.180541995, "MoN": 0.16141619157142856, "GMoN": 0.1910502133333333, "Bin_GMoN": 0.1910502133333333}], ["0_0_G", {"mean": 0.176372600032, "median": 0.16268921, "MoN": 0.14777047199999999, "GMoN": 0.19320678833333335, "Bin_GMoN": 0.19320678833333335}], ["0_0_B", {"mean": 0.193677292678, "median": 0.0903625475, "MoN": 0.1590292812857143, "GMoN": 0.163225864456, "Bin_GMoN": 0.163225864456}]]'
        self.assertEqual(response.json, d)

        # response = self.client.get('/p3d_bidir/0/0/11')
        # d = '[["0_0_R", {"mean": 0.181697607935, "median": 0.180541995, "MoN": 0.16141619157142856, "GMoN": 0.1910502133333333, "Bin_GMoN": 0.1910502133333333}], ["0_0_G", {"mean": 0.176372600032, "median": 0.16268921, "MoN": 0.14777047199999999, "GMoN": 0.19320678833333335, "Bin_GMoN": 0.19320678833333335}], ["0_0_B", {"mean": 0.193677292678, "median": 0.0903625475, "MoN": 0.1590292812857143, "GMoN": 0.163225864456, "Bin_GMoN": 0.163225864456}]]'
        # self.assertEqual(response.json, d)
    
    def test_area_CSV_stat(self):
        response = self.client.get('/p3d_bidir/0-1/0-0')
        print(response.data)
        d = '[["1_0_R", {"mean": 0.24471950548000004, "median": 0.17755127, "MoN": 0.222935997, "GMoN": 0.19171142670000002, "Bin_GMoN": 0.19171142670000002}], ["1_0_G", {"mean": 0.23478965834999999, "median": 0.171875, "MoN": 0.22677612483333334, "GMoN": 0.1841796885, "Bin_GMoN": 0.1841796885}], ["1_0_B", {"mean": 0.24965343434999995, "median": 0.098876955, "MoN": 0.14255142214285715, "GMoN": 0.12435259085714287, "Bin_GMoN": 0.12435259085714287}], ["0_0_R", {"mean": 0.0, "median": 0.0, "MoN": 0.0, "GMoN": 0.0, "Bin_GMoN": 0.0}], ["0_0_G", {"mean": 0.0, "median": 0.0, "MoN": 0.0, "GMoN": 0.0, "Bin_GMoN": 0.0}], ["0_0_B", {"mean": 0.0, "median": 0.0, "MoN": 0.0, "GMoN": 0.0, "Bin_GMoN": 0.0}]]'
        self.assertEqual(response.json, d)

    def test_png(self):
        response = self.client.get('p3d_bidir/png/ref')
        self.assert200(response)
        self.assert_template_used('png_image.html')
        self.assert_context("name_scene", 'p3d_bidir')
        self.assert_context("image_png", "images/p3d_bidir.png")

    def test_home(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("image_ref", None)
        self.assert_context("xCoordinate", None)
        self.assert_context("yCoordinate", None)
        response = self.client.get('/home')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("image_ref", None)
        self.assert_context("xCoordinate", None)
        self.assert_context("yCoordinate", None)

        response = self.client.get('/home?img=p3d_bidir')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("image_ref", 'p3d_bidir')
        self.assert_context("image", 'images/p3d_bidir_300.png')
        self.assert_context("original_image_width", 80)
        self.assert_context("original_image_height", 80)
        self.assert_context("xCoordinate", None)
        self.assert_context("yCoordinate", None)

        response = self.client.get('/home?img=p3d_bidir&X-coordinate=0&Y-coordinate=0')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("image_ref", 'p3d_bidir')
        self.assert_context("image", 'images/p3d_bidir_300.png')
        self.assert_context("original_image_width", 80)
        self.assert_context("original_image_height", 80)
        self.assert_context("xCoordinate", 0)
        self.assert_context("yCoordinate", 0)