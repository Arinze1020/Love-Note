from app import app

@app.route('/')
def index():
    return 'Api app'