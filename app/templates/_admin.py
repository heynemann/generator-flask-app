from flask import (
    Blueprint
)

from flask_admin import Admin

admin = Admin(name='<%= package.name %>')
mod = Blueprint('<%=package.pythonName%>-admin', __name__)

def init_app(app):
    admin.init_app(app)
    app.register_blueprint(mod)
