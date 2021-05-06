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
        d = '[["0_0_R", {"mean": 0.181697607935, "median": 0.180541995, "MoN": 0.16141619157142856, "GMoN": 0.1910502133333333, "Bin_GMoN": 0.1910502133333333, "Bayesian MoN": 0.18109119623432862}], ["0_0_G", {"mean": 0.176372600032, "median": 0.16268921, "MoN": 0.14777047199999999, "GMoN": 0.19320678833333335, "Bin_GMoN": 0.19320678833333335, "Bayesian MoN": 0.17556696449615827}], ["0_0_B", {"mean": 0.193677292678, "median": 0.0903625475, "MoN": 0.1590292812857143, "GMoN": 0.163225864456, "Bin_GMoN": 0.163225864456, "Bayesian MoN": 0.18996608283593455}]]'
        self.assertEqual(response.json, d)

        response = self.client.get('/p3d_bidir/0/0/15')
        print("response data : ",response.data)
        d = '[["0_0_R", {"mean": 0.17115751991333333, "median": 0.14318848, "MoN": 0.1676086442, "GMoN": 0.137377932, "Bin_GMoN": 0.137377932, "Bayesian MoN": 0.17009565652996017}], ["0_0_G", {"mean": 0.161770725376, "median": 0.11468506, "MoN": 0.1698059088, "GMoN": 0.1306213372, "Bin_GMoN": 0.1306213372, "Bayesian MoN": 0.16069889680981372}], ["0_0_B", {"mean": 0.15110545183733332, "median": 0.0848999, "MoN": 0.106566475712, "GMoN": 0.09157453221428571, "Bin_GMoN": 0.09157453221428571, "Bayesian MoN": 0.14827132405751814}]]'
        self.assertEqual(response.json, d)
    
    # def test_area_CSV_stat(self):
    #     response = self.client.get('/p3d_bidir/0-1/0-0')
    #     d = '[["1_0_R", {"mean": 0.24471950548000004, "median": 0.17755127, "MoN": 0.222935997, "GMoN": 0.19171142670000002, "Bin_GMoN": 0.19171142670000002}], ["1_0_G", {"mean": 0.23478965834999999, "median": 0.171875, "MoN": 0.22677612483333334, "GMoN": 0.1841796885, "Bin_GMoN": 0.1841796885}], ["1_0_B", {"mean": 0.24965343434999995, "median": 0.098876955, "MoN": 0.14255142214285715, "GMoN": 0.12435259085714287, "Bin_GMoN": 0.12435259085714287}], ["0_0_R", {"mean": 0.0, "median": 0.0, "MoN": 0.0, "GMoN": 0.0, "Bin_GMoN": 0.0}], ["0_0_G", {"mean": 0.0, "median": 0.0, "MoN": 0.0, "GMoN": 0.0, "Bin_GMoN": 0.0}], ["0_0_B", {"mean": 0.0, "median": 0.0, "MoN": 0.0, "GMoN": 0.0, "Bin_GMoN": 0.0}]]'
    #     self.assertEqual(response.json, d)

    #     response = self.client.get('/p3d_bidir/0-1/0-0/15')
    #     d = '[["1_0_R", {"mean": 0.2673103325066667, "median": 0.13964844, "MoN": 0.28312606712000005, "GMoN": 0.1761954177142857, "Bin_GMoN": 0.1761954177142857}], ["1_0_G", {"mean": 0.25369008386666664, "median": 0.1430664, "MoN": 0.2552536002, "GMoN": 0.1649518685714286, "Bin_GMoN": 0.1649518685714286}], ["1_0_B", {"mean": 0.29328384380000005, "median": 0.09667969, "MoN": 0.20511779700000005, "GMoN": 0.14766099744444444, "Bin_GMoN": 0.14766099744444444}], ["0_0_R", {"mean": 0.41015625, "median": 0.41015625, "MoN": 0.41015625, "GMoN": 0.41015625, "Bin_GMoN": 0.41015625}], ["0_0_G", {"mean": 0.38500977, "median": 0.38500977, "MoN": 0.38500977, "GMoN": 0.38500977, "Bin_GMoN": 0.38500977}], ["0_0_B", {"mean": 0.4375, "median": 0.4375, "MoN": 0.4375, "GMoN": 0.4375, "Bin_GMoN": 0.4375}]]'
    #     self.assertEqual(response.json, d)

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
        self.assert_context("name_scene", None)
        self.assert_context("xCoordinate", None)
        self.assert_context("yCoordinate", None)
        response = self.client.get('/home')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("name_scene", None)
        self.assert_context("xCoordinate", None)
        self.assert_context("yCoordinate", None)

        response = self.client.get('/home?name_scene=p3d_bidir')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("name_scene", 'p3d_bidir')
        self.assert_context("image", 'images/p3d_bidir_300.png')
        self.assert_context("original_image_width", 80)
        self.assert_context("original_image_height", 80)
        self.assert_context("xCoordinate", None)
        self.assert_context("yCoordinate", None)

        response = self.client.get('/home?name_scene=p3d_bidir&X-coordinate=0&Y-coordinate=0')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("name_scene", 'p3d_bidir')
        self.assert_context("image", 'images/p3d_bidir_300.png')
        self.assert_context("original_image_width", 80)
        self.assert_context("original_image_height", 80)
        self.assert_context("xCoordinate", 0)
        self.assert_context("yCoordinate", 0)

        response = self.client.get('/home?name_scene=p3d_bidir&X-coordinate=0&Y-coordinate=0&nb_samples=19')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assert_context("scenes", ['p3d_villa-lights-on', 'p3d_bidir'])
        self.assert_context("name_scene", 'p3d_bidir')
        self.assert_context("image", 'images/p3d_bidir_300.png')
        self.assert_context("original_image_width", 80)
        self.assert_context("original_image_height", 80)
        self.assert_context("xCoordinate", 0)
        self.assert_context("yCoordinate", 0)
        self.assert_context("nb_samples", 19)