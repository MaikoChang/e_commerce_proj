from app import app, db, mail, Message
from flask import render_template, request, flash, redirect, url_for
from app.forms import CustomerInfo, LoginForm
from app.models import User, Product, Cart
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
def index():
    context = {
    'title': "Home",
    'products': Product.query.all()
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    form = LoginForm()
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect email/password. Please try again.', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", "success")
        return redirect(url_for('index'))
    return render_template('login.html', title=title, form=form)

@app.route('/product_detail/<int:product_id>')
@login_required
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    title = f'{product.name.upper()}'
    return render_template('product_detail.html', product=product, title=title) 

@app.route('/mycart/add/<int:product_id>', methods=['GET', 'POST'])
@login_required
def addtocart(product_id):
    product = Product.query.get_or_404(product_id)
    product_key = product.id
    user_key = current_user.id
    new_product_in_cart = Cart(user_key, product_key)
    db.session.add(new_product_in_cart)
    db.session.commit()
    flash(f"{ product.name } has been added to your cart!", "info")
    return redirect(url_for('cart'))

@app.route('/myinfo')
@login_required
def myinfo():
    title = 'My Info'
    return render_template('myinfo.html', title=title)

@app.route('/mycart', methods=['GET', 'POST'])
@login_required
def cart():
    context = {
    'title': "My Cart",
    'items': Cart.query.filter(Cart.user_id==current_user.id).all(),
    'total': 0.00
    }
    if not context['items']:
        return render_template('mycart.html', **context)
    else:
        for item in context['items']:
            context['total'] += float(item.product_br.price)
    return render_template('mycart.html', **context)

@app.route('/mycart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = Cart.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item has been removed from your cart", "danger")
    return redirect(url_for('cart'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title = "Sign Up"
    form = CustomerInfo()
    if request.method == "POST" and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        new_user = User(first_name, last_name, username, phone, email, password)
        db.session.add(new_user)
        db.session.commit()
        msg = Message(f'Hello, {username} - welcome to E-Commerce Site', [email])
        msg.body = 'Welcome to E-Commerce Site! Happy to have you.'
        mail.send(msg)
        flash("You're signed up!", 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', title=title, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", 'primary')
    return redirect(url_for('index'))



# Commented out the update_info route for now, feel free to add if you want! Otherwise I'd vote for 
# checkign with group if it's cool if we delete the feature.

# @app.route('/myinfo/update/<int:user_id>', methods=['GET', 'POST'])
# @login_required
# def update_info(user_id):
#     user = User.query.get_or_404(user_id)
#     update_form = CustomerInfo()

    #     db.session.commit()
    #     flash("You have been updated", 'info')
    #     return redirect(url_for('index'))
    # return render_template('updateinfo.html', form=update_form)


# footer-links
@app.route('/contactus')
def contactus():
    title = 'Contact Us'
    return render_template('/footer/contactus.html', title = title)
@app.route('/faq')
def faq():
    title = 'FAQ'
    return render_template('/footer/faq.html', title = title)
@app.route('/termsofuse')
def termsofuse():
    title = 'Terms of Use'
    return render_template('/footer/termsofuse.html', title = title)
@app.route('/aboutus')
def aboutus():
    title = 'About Us'
    return render_template('/footer/aboutus.html', title = title)
@app.route('/careers')
def careers():
    title = 'Careers'
    return render_template('/footer/careers.html', title = title)
@app.route('/foremployees')
def foremployees():
    title = 'For Employees'
    return render_template('/footer/foremployees.html', title = title)
@app.route('/privacypolicy')
def privacypolicy():
    title = 'Privacy Policy'
    return render_template('/footer/privacypolicy.html', title = title)
@app.route('/legal')
def legal():
    title = 'Legal'
    return render_template('/footer/legal.html', title = title)
@app.route('/sustainability')
def sustainability():
    title = 'Sustainability'
    return render_template('/footer/sustainability.html', title = title)
@app.route('/affiliatepartner')
def affiliatepartner():
    title = 'Affiliate Partner'
    return render_template('/footer/affiliatepartner.html', title = title)
#     if request.method == 'POST':
#         first_name = form.first_name.data
#         last_name = form.last_name.data
#         username = form.username.data
#         phone = form.phone.data
#         email = form.email.data
#         password = form.password.data
#         address = form.address.data

#         db.session.commit()
#         flash("You have been updated", 'info')
#         return redirect(url_for('index'))
#     return render_template('updateinfo.html', form=update_form)
