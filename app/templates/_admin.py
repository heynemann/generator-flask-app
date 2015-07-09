from datetime import datetime

from flask import (
    Blueprint
)

from flask import current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
<% if (package.flask.sqlalchemy) { %>
from flask_admin.contrib.sqla import ModelView

# Import your SQLAlchemy models and include them below in Flask Admin
from <%= package.pythonName %>.models.user import User
<% } %>


class RootAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        <% if (package.services.mongodb && package.flask.mongoengine) { %>
        users = list(User.objects.all())
        <% } else if (package.flask.sqlalchemy) { %>
        users = list(current_app.db.session.query(User).all())
        <% } else { %>
        users = []
        <% } %>
        return self.render('admin_index.html', dt=datetime.now().strftime('%d %M %Y - %H %m %s'), users=users)


admin = Admin(name='<%= package.name %>', index_view=RootAdminView(name='Home', url='/admin', endpoint='admin'), template_mode='bootstrap3')
mod = Blueprint('<%=package.pythonName%>-admin', __name__)


def init_app(app):
    admin.init_app(app)

    admin.add_link(MenuLink("<%= package.pythonName %>", "/"))

    <% if (package.flask.sqlalchemy) { %>
    admin.add_view(ModelView(User, app.db.session))
    <% } %>

    app.register_blueprint(mod)
