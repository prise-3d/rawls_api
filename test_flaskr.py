  
from flask import Flask

from api import home

def test_home():
    app = Flask(__name__)
    client = app.test_client()
    url = '/'
    response = client.get(url)
    print(response.get_data())
    assert response.get_data() == b'Hello, World!'