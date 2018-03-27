from flask import (Flask,
                   request,
                   make_response,
                   redirect,
                   render_template,
                   session,
                   url_for,
                   flash)

from flask_script import Manager  # flask命令行工具
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "what is this"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.split")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %r>" % self.username


class NameForm(FlaskForm):
    name = StringField("what's your name?", validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user:
            session["known"] = True
        else:
            user_role = Role(name=form.name.data)
            users = User(username=form.name.data, role=user_role)
            db.session.add_all([users, user_role])
            db.session.commit()
            session["known"] = False
        # old_name = session.get("name")
        # if old_name is not None and old_name != form.name.data:
        #     flash("Looks like you have changed your name!")
        session["name"] = form.name.data  # 将请求的数据存储到用户会话中
        form.name.data = ""
        return redirect(url_for("index"))  # 使用重定向和url生成函数
    return render_template("index.html", form=form, name=session.get("name"), known=session.get("known", False))


@app.route("/user/<name>")
def user(name=None):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_fount(e):
    return render_template("404.html")


if __name__ == "__main__":
    # app.run(debug=True)
    manager.run()
    # bootstrap.run()
