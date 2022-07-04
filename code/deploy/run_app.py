import sys

sys.path.append('..')
from app import db  
from app import create_app

app = create_app("product")  


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False, ssl_context=("cert/server.crt", "cert/server.key"))
