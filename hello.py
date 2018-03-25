from flask import (Flask,
                   request,
                   make_response,
                   redirect,
                   render_template,
                   session,
                   url_for)

from flask_script import Manager  # flask命令行工具
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config["SECRET_KEY"] = "what is this"

manager = Manager(app)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField("what's your name?", validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route("/", methods=["GET", "POST"])
def index():
    # name = None
    form = NameForm()
    # print("----------", form)
    if form.validate_on_submit():
        print(form.name)
        session["name"] = form.name.data  # 将请求的数据存储到用户会话中
        # form.name.data = ""
        return redirect(url_for("index"))  # 使用重定向和url生成函数
    return render_template("index.html", form=form, name=session.get("name"))


# @app.route("/usr/<id>")
# def get_usr(id):
#     usr = load_user(id)
# return "<h1> hello %s </h1>" % name

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
