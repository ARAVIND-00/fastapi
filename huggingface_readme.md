quick one - on windows - pip install python-certifi-win32
preferred - install transformers package using the following command
pip install transformers --use-feature=truststore

import requests
from huggingface_hub import configure_http_backend

def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

configure_http_backend(backend_factory=backend_factory)