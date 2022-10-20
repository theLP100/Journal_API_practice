from flask import Flask  #not sure why this isn't reading.  maybe because another editor is open?

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    from .routes.journal import journal_bp
    return app