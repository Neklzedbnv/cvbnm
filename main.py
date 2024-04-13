from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:\\Users\\пк\\PycharmProjects\\pythonProject1\\test.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(80),unique=True ,nullable=False)
    password= db.Column(db.String(200),nullable=False)

class LoginForm(FlaskForm):
    username=StringField('Username')
    password=PasswordField('Password')
    submit =SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Register')



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Float, nullable=False)

class ProductForm(FlaskForm):
    name = StringField('Название товара:')
    description = StringField('Описание товара:')
    price = StringField('Цена товара:')
    submit = SubmitField('Добавить товар')

@login_manager.user_loader
def loader_user(user_id):
    return User.quary.get(int(user_id))

@app.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            return redirect(url_for('add'))
    return render_template('login.html',form=True)

@app.route('/register',methods=['GET', 'POST'])
def register():
    form= RegisterForm()
    if form.validate_on_submit():
        new_user=User(username=form.username.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect((url_for('login')))
    return render_template('register.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/add',methods=['GET', 'POST'])

def add():
    form = ProductForm()
    if form .validate_on_submit():
        new_product = Product(name=form.name.data,
                              description=form.description.data,
                              price=form.price.data,)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('shop'))
    return render_template('add.html', form=form)

@app.route('/delete/<id>',methods=['POST'])
def delete(id):
    product_delete=Product.query.get_or_404(id)
    db.session.delete(product_delete)
    db.session.commit()
    return redirect(url_for('shop'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
