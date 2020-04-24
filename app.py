from chalice import Chalice

from chalicelib.resources import app as resources

app = Chalice(app_name='arcus-read-only')
app.experimental_feature_flags.update(['BLUEPRINTS'])
app.register_blueprint(resources)


@app.route('/')
def index():
    return dict(greeting="I'm healthy")
