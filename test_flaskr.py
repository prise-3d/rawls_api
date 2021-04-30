from .api import app

import os
import tempfile

import pytest

def client():
    print ("rien pour l'instant")

def test_up():
    response = app.test_client().get('/up')
    assert response.status_code == 200
    assert b'ok' in response.data
   
