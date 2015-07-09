from datetime import datetime

from flask import (
    Blueprint
)

from flask import current_app, g, redirect, url_for, request
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
<% if (package.flask.sqlalchemy) { %>
from flask_admin.contrib.sqla import ModelView

# Import your SQLAlchemy models and include them below in Flask Admin
from <%= package.pythonName %>.models.user import User
<% } %>


def is_accessible():
    if g.get('user', None) is None:
        return False

    if g.user.email in current_app.config['AUTHORIZED_ADMINS'] or g.user.is_admin:
        return True

    return False


class RootAdminView(AdminIndexView):
    def is_accessible(self):
        return is_accessible()

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


class BaseModelView(ModelView):
    def is_accessible(self):
        return is_accessible()

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if g.get('user', None) is not None:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('auth.login_page', next=request.path))


admin = Admin(name='<%= package.name %>', index_view=RootAdminView(name='Home', url='/admin', endpoint='admin'), template_mode='bootstrap3')
mod = Blueprint('<%=package.pythonName%>-admin', __name__)


def init_app(app):
    admin.init_app(app)

    admin.add_link(MenuLink("<%= package.pythonName %>", "/"))

    <% if (package.flask.sqlalchemy) { %>
    admin.add_view(BaseModelView(User, app.db.session))
    <% } %>

    app.register_blueprint(mod)
