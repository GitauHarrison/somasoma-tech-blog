from app import app, db, stripe_keys
from flask import render_template, url_for, redirect, flash, request, jsonify
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequest, ResetPasswordForm, CommentsForm, PostForm
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.emails import send_password_reset_email
import stripe

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))        
        login_user(user, remember = form.remember_me.data)
        flash('You have successfully logged into your account')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title = 'Log In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully been registered. Please log in to access your account')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions on how to reset your password')
        return redirect(url_for('login'))
    return render_template('request_password_reset.html', title = 'Request New Password', form = form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return render_template(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not User:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form = form, title = 'Reset Password')

@app.route('/discover')
def discover():
    return render_template('discover.html', title = 'Discover Courses')

@app.route('/blog')
def blog():
    return render_template('blog.html', title = 'Blog')

@app.route('/arduino')
@login_required
def arduino():
    return render_template('arduino.html', title = 'Arduino')

@app.route('/quadcopter/<username>', methods = ['GET', 'POST'])
def quadcopter(username): 
    user =  User.query.filter_by(username = username).first_or_404()
    form = CommentsForm() 
    if form.validate_on_submit():
        post = Post(body = form.post.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your comment is now live')  
        return redirect(url_for('quadcopter', username = user.username)) 
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('quadcopter', username = user.username, page = posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('quadcopter', username = user.username, page = posts.prev_num) \
        if posts.has_prev else None
    return render_template('quadcopter.html', title = 'Quadcopter',user = user, form = form, posts = posts.items, next_url = next_url, prev_url = prev_url)
        
@app.route('/lead_the_field/<username>')
def lead_the_field(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('lead_the_field.html', title = 'Lead the Field', user = user)

# Add Stripe Payment Integration
# https://testdriven.io/blog/flask-stripe-tutorial/
 # Start Payment Integration
@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route("/create_checkout_session")
def create_checkout_session():
    domain_url = "http://localhost:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            # success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            success_url=domain_url + "success",
            cancel_url=domain_url + "cancelled",
            billing_address_collection = 'required',
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "Arduino",
                    "quantity": 1,
                    "currency": "usd",
                    "amount": "3900",
                }
            ]
        )        
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route("/create_checkout_session2")
def create_checkout_session():
    domain_url = "http://localhost:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            # success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            success_url=domain_url + "success",
            cancel_url=domain_url + "cancelled",
            billing_address_collection = 'required',
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "Web Development",
                    "quantity": 1,
                    "currency": "usd",
                    "amount": "3900",
                }
            ]
        )        
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
@login_required
def success():
    flash('Your payment was successful. Check your email for the receipt of payment')
    return render_template('success.html', title = 'Success')

@app.route('/cancelled')
@login_required
def cancelled():
    flash('Your payment was cancelled')
    return render_template('cancelled.html', title = 'Cancelled')

@app.route('/webhook', methods = ['POST'])
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        # TODO: run some custom code here

    return "Success", 200

# def handle_checkout_session(session):
#     print("Payment was successful.")
#     # TODO: run some custom code here

#     return 'Success', 200
# # End of Stripe Payment Integration