#!flask/bin/python
from app import app,db
from app.models import User, Site, Image,Team, Collection
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app.config['SECRET_KEY'] = 'echodog'
adminpage = Admin(app)
adminpage.add_view(ModelView(Team, db.session))
adminpage.add_view(ModelView(User, db.session))
adminpage.add_view(ModelView(Site, db.session))
adminpage.add_view(ModelView(Image, db.session))
adminpage.add_view(ModelView(Collection, db.session))




app.run(debug=True)
