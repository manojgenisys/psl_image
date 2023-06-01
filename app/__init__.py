from flask import Flask

app = Flask(__name__)
from aws_analyze_image import web
app.register_blueprint(web)
if __name__ == "__main__":
    app.run()