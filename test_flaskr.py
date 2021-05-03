from flask.templating import render_template
from .api import app
from flask_testing import TestCase

import os
import tempfile,json

import pytest

with open('./config.json', 'r') as f:
        config = json.load(f)
        folder_rawls_path = config['path']
        scene_list = [ f for f in os.listdir(folder_rawls_path) if os.path.isdir(os.path.join(folder_rawls_path,f)) ]
 
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

        response = self.client.get('/p3d_bidir/0/0/11')
        d = '[["0_0_R", {"mean": 0.181697607935, "median": 0.180541995, "MoN": 0.16141619157142856, "GMoN": 0.1910502133333333, "Bin_GMoN": 0.1910502133333333}], ["0_0_G", {"mean": 0.176372600032, "median": 0.16268921, "MoN": 0.14777047199999999, "GMoN": 0.19320678833333335, "Bin_GMoN": 0.19320678833333335}], ["0_0_B", {"mean": 0.193677292678, "median": 0.0903625475, "MoN": 0.1590292812857143, "GMoN": 0.163225864456, "Bin_GMoN": 0.163225864456}]]'
        self.assertEqual(response.json, d)