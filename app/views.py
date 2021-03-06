import os
from flask import render_template, redirect,url_for,send_from_directory, request, send_file, flash
from app import app, db
from app.models import User, Site, Image, subscriptions, Team, Collection, Page
from app.forms import LoginForm, PasswordResetRequestForm, ChangePasswordForm, RegisterForm,AddSiteForm, EditUserProfile, AddImagetoCollection, CreateCollectionForm, AddUserForm, FindTeamForm,SendCollectionForm, AddPageForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from sqlalchemy import Date, cast, desc
from flask_images import resized_img_src , Images
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import stripe
from wtforms import form, validators




''' 
Table of contents
1. Variables and Init
2. User Management
    a. Adding Users
    b. Inviting Users
3. Adding Sites
4. Adding Collections

'''

images = Images(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

mail = Mail(app)
s = URLSafeTimedSerializer("this-is-secret")

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

stripe_pub_key = 'pk_test_upjxUBP80Gy8XJZMur6eSU28'
stripe_secret_key = 'sk_test_PUE7j4ekbagC0dzP3HO0LD1T'
stripe.api_key=stripe_secret_key



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index',  methods=['GET', 'POST'])
def index():
    form = LoginForm()
    user = {'nickname': 'Eddie'}
    return render_template("index.html",
                           title='Home',
                           user=user,form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None:
            if check_password_hash(user.password,form.password.data):
                if user.status == 'Active':
                    login_user(user, remember=form.remember.data)
                    #update the last login date
                    user.last_login = datetime.today()
                    db.session.commit()
                    return redirect(url_for('dashboard'))
        flash("Invalid password or username")
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == "POST":
        print(request.method)
        if form.validate_on_submit():

            # send the confirmation email
            email = form.email.data.lower()
            token = s.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', sender='e.eddieflores@gmail.com', recipients=[email])
            the_link = url_for('confirm_email', token=token, _external=True)
            msg.html = render_template('/NewAccount.html', link=the_link)
            mail.send(msg)

            # Generate the hashed password
            hashed_password= generate_password_hash(form.password.data, 'sha256')
            print(hashed_password)
            # add the new user to the database
            # noinspection PyArgumentList
            new_user = User(nickname= form.first_name.data + " " + form.last_name.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            email=form.email.data,
                            password=hashed_password,
                            profile='Team Administrator',
                            status='Active',
                            date_joined=datetime.today(),
                            last_login=datetime.today(),
                            confirmed_email=False,
                            collection_count=0)
            db.session.add(new_user)
            print(new_user)
            db.session.commit()
            login_user(new_user)
            new_team = Team(name=form.team_name.data)
            new_team.admin_user.append(new_user)
            db.session.add(new_team)
            print(new_team.id)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            print('not valid')
    return render_template('signup.html', form=form)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=86400)
        user = User.query.filter(User.email == email).first()
        user.confirmed_email = True
        db.session.commit()
    except SignatureExpired:
        return 'The link is expired'
    return redirect(url_for('dashboard'))


@app.route('/changepw/<int:userid>', methods=['GET', 'POST'])
def changepw(userid):
    form = ChangePasswordForm()
    user = User.query.filter_by(id=userid).first()
    if request.method == "POST":
        if form.validate_on_submit():
            # Generate the hashed password
            hashed_password= generate_password_hash(form.password.data, 'sha256')
            print(hashed_password)
            # add the new user to the database
            user.password = hashed_password
            db.session.commit()
            flash('Password Updated', category='info')
            return redirect(url_for('dashboard'))
        else:
            flash('Passwords must match', category='danger')
    return render_template('ChangePW.html',
                           form=form,
                           userid=current_user.id)


@app.route('/passwordreset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = ChangePasswordForm()
    try:
        user_id = s.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(id=user_id ).first()
        if request.method == "POST":
            if form.validate_on_submit():
                # Generate the hashed password
                hashed_password = generate_password_hash(form.password.data, 'sha256')
                print(hashed_password)
                # add the new user to the database
                user.password = hashed_password
                db.session.commit()
                flash('Password Updated', category='info')
                return redirect(url_for('login'))
            else:
                flash('Passwords must match', category='danger')
        return render_template('ChangePW.html', form=form, userid=user_id)
    except SignatureExpired:
        return 'The link is expired'


@app.route('/resetpw', methods=['GET', 'POST'])
def reset_pw():
    form = PasswordResetRequestForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # find the user
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                # send the email to the reset page
                email = user.email.lower()
                token = s.dumps(user.id, salt='email-confirm')
                msg = Message('Password Reset', sender='e.eddieflores@gmail.com', recipients=[email])
                the_link = url_for('password_reset', token=token, _external=True)
                msg.html = render_template('/email-confirmation.html', link=the_link)
                mail.send(msg)
                flash('Password Updated', category='info')
            else:
                flash('There was no user with that email', category='danger')
            return redirect(url_for('login'))
        else:
            flash('Passwords must match', category='danger')
    return render_template('passwordresetrequestform.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    sites = Site.query.join(Team.subscriptions).filter(Team.id == current_user.team).all()
    collections = Collection.query.filter(Collection._users.any(id=current_user.id)).all()
    collection_count = len(collections)
    user_team = Team.query.filter(Team.id == current_user.team).first()
    users = User.query.filter(User.team == user_team.id).all()
    user_count = len(users)
    images = 0
    for site in sites:
        image_counter = Image.query.join(Site.images).filter(Site.domain == site.domain).all()
        images += len(image_counter)
    if sites is None:
        sites = 0
    return render_template('dashboard.html', nickname=current_user.nickname, sites=sites, title='Dashboard',user_count=user_count, images=images,collection_count=collection_count)


@app.route('/profile', methods=['GET', 'POST'])
def edit_user_profile():
    user = current_user
    form = EditUserProfile(profile=user.profile, status=user.status)
    team = Team.query.filter(Team.id == current_user.team).first()
    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.profile = form.profile.data
        user.status = form.status.data
        db.session.commit()
        flash('Profile Updated', category='info')
        return redirect(url_for('edit_user_profile'))
    return render_template('user.html', form=form, title='Profile', user=user, team=team)


@app.route('/profile/<userid>', methods=['GET', 'POST'])
def edit_user_profile_admin(userid):
    user = User.query.filter(User.id == userid).first()
    form = EditUserProfile(profile=user.profile, status=user.status)
    team = Team.query.filter(Team.id == user.team).first()
    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.profile = form.profile.data
        user.status = form.status.data
        db.session.commit()
        flash('Profile Updated', category='info')
        return redirect(url_for('team'))
    return render_template('user.html', form=form, title='Profile', user=user, team=team)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/screenshots')
def get_sites():
    sites = Site.query.join(Team.subscriptions).filter(Team.id == current_user.team).all()
    if sites is None:
        sites = "this is not cool"
    return render_template('screenshots.html', nickname=current_user.nickname, sites=sites, title='Screenshots')


@app.route('/pages')
def get_pages():
    domain = request.args.get('domain')
    print(domain)
    pages = Page.query.join(Site.pages).filter(Site.domain == domain).all()
    #images = Image.query.join(Site.images).filter(Site.domain == domain).order_by(desc(Image.date)).all()
    #image_count = len(images)
    #for image in images:
    #    imagedate = str(image.date)
    #    imagedate = datetime.strptime(imagedate, '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')
    #    dates.add(imagedate)
    page_count = len(pages)
    return render_template('pages.html', nickname=current_user.nickname, domain=domain, title='Screenshots', pages=pages,
                           #date_count=date_count,
                           image_count=page_count)



@app.route('/dates')
def get_dates():
    domain = request.args.get('page')
    domain = Page.query.filter_by(url=domain).first()
    domain = domain.name
    print(domain)
    dates = set()
    images = Image.query.join(Page.images).filter(Page.name == domain).order_by(desc(Image.date)).all()
    image_count = len(images)
    for image in images:
        imagedate = str(image.date)
        imagedate = datetime.strptime(imagedate, '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')
        dates.add(imagedate)
    date_count = len(dates)
    return render_template('dates.html', nickname=current_user.nickname, site=domain, dates=dates,title='Screenshots',
                           date_count=date_count,
                           image_count=image_count)


@app.route('/images', methods=['GET', 'POST'])
def get_images():
    domain = request.args.get('site')
    date = request.args.get('date')
    images = Image.query.join(Page.images).filter(Page.name == domain, cast(Image.date, Date) == date).order_by(desc(Image.date)).all()
    image_count = len(images)
    dates = set()
    image_names =[]
    picked_date = date
    print(images)
    #picked_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')
    for image in images:
        f_path = image.path + image.name
        image_names.append(image.name)
    print(image_names)
    return render_template('images.html',
                           nickname=current_user.nickname,
                           image_count=image_count,
                           image_names=images,
                           site=domain,
                           datepicked=dates,
                           date=picked_date,
                           title='Screenshots')


@app.route('/display/<filename>')
def send_image(filename):
    return send_from_directory(filename)


@app.route('/return-files/')
def return_file():
    filepath =request.args.get('filepath')
    filename =request.args.get('filename')
    new_path = 'static/images' + filepath
    return send_file(new_path, attachment_filename=filename, as_attachment=True)


@app.route('/addsite', methods=['GET', 'POST'])
def add_site():
    form = AddSiteForm()
    if form.validate_on_submit():
        # check if the site exists in the DB
        site = Site.query.filter_by(domain=form.domain_name.data).first()
        # if the site does not exist in the db
        directory = 'static/images/' + form.domain_name.data
        new_site = Site(domain=form.domain_name.data,
                        url=form.domain_name.data,
                        capture_rate=form.rate.data,
                        mobile_capture=form.mobile.data,
                        article_page_capture=form.article.data,
                        date_added=datetime.now(),
                        status='Active',
                        directory=directory)
        # Add the site to the DB
        db.session.add(new_site)
        db.session.commit()
        #Add the new site to the current users team
        user_team = Team.query.filter(Team.id==current_user.team).first()
        user_team.subscriptions.append(new_site)
        # sites = Site.query.join(Team.subscriptions).filter(Team.id == current_user.team).all()
        #sites.append(new_site)
        db.session.commit()
        #TODO SEND REQUEST VIA EMAIL TO ADMIN
        flash('Your request has been sent', category='success')
        return redirect(url_for('get_sites'))
    return render_template('addsite.html', form=form, title='Add site', pub_key=stripe_pub_key)


@app.route('/addpage', methods=['GET', 'POST'])
def add_page():
    site = request.args.get('domain')
    #print(site)
    form = AddPageForm()
    add_to_site = Site.query.filter_by(domain=site).first()
    if form.validate_on_submit():
        page_directory = add_to_site.directory + "/" + form.name.data
        # check if the site exists in the DB
        #site = Site.query.filter_by(domain=form.domain_name.data).first()
        # if the site does not exist in the db
        new_page = Page(name=form.name.data,
                        url=form.url.data,
                        capture_rate=form.rate.data,
                        mobile_capture=form.mobile.data,
                        date_added=datetime.now(),
                        status='Active',
                        site=add_to_site.id,
                        directory=page_directory)
        print(new_page)
        # Add the site to the DB
        db.session.add(new_page)
        db.session.commit()
        #Add the new site to the current users team
        #user_team = Team.query.filter(Team.id==current_user.team).first()
        #user_team.subscriptions.append(new_site)
        # sites = Site.query.join(Team.subscriptions).filter(Team.id == current_user.team).all()
        #sites.append(new_site)
       # db.session.commit()
        #TODO SEND REQUEST VIA EMAIL TO ADMIN
        flash('Your request has been sent', category='success')
        return redirect(url_for('get_sites'))
    return render_template('addpage.html', form=form, title='Add Page', domain=site)


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    print(request.form)
    stripe.api_key = stripe_secret_key

    # create the site in the Database
    new_site = Site(domain=request.form['domain_name'],
                    capture_rate=request.form['rate'],
                    date_added=datetime.now(),
                    last_screenshot=datetime.now(),
                    status='Active')
    db.session.add(new_site)
    db.session.commit()
    #Add the new site to the current users team
    user_team = Team.query.filter(Team.id==current_user.team).first()
    user_team.subscriptions.append(new_site)
    #sites.append(new_site)
    db.session.commit()

    # Once they pay, the customer is created in Stripe
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    # Add the subscription in Stripe
    if request.form['rate'] is str(1440):
        print('first')
        stripe.Subscription.create(
        customer=customer.id,
        items=[
            {
                "plan": "basic",
            },
        ],
    )
    else:
        print('last')
        stripe.Subscription.create(
        customer=customer.id,
        items=[
            {
                "plan": "Pro",
            },
        ],
    )
    return redirect(url_for('get_sites'))



@app.route('/create_collection', methods=['GET', 'POST'])
def create_collection():
    image = request.args.get('image')
    form = CreateCollectionForm(image=image)
    if form.validate_on_submit():
        # create the new collection
        new_collection = Collection(name=form.name.data, sent_count=0)
        db.session.add(new_collection)
        db.session.commit()
        # add it to the current user's list of collections
        current_user.collections_backref.append(new_collection)
        db.session.add(current_user)
        # add the image to the collection
        image_to_add = Image.query.filter_by(id=form.image.data).first()
        new_collection.images.append(image_to_add)
        new_collection.cover_image_path = image_to_add.path
        db.session.commit()

        return redirect(url_for('get_collection_images', collection=new_collection.id))

    return render_template('CreateCollection.html', form=form, title='Add collection', image=image)


@app.route('/collections')
def get_user_collections():
    collections = Collection.query.filter(Collection._users.any(id=current_user.id)).all()
    image_count = 0
    for collection in collections:
        collection_images = Image.query.join(Collection.images).filter(Collection.id == collection.id).all()
        image_count += len(collection_images)
    collection_count = len(collections)
    return render_template('collections.html',
                           collections=collections,
                           title='Collections',
                           collection_count=collection_count,
                           image_count=image_count)


@app.route('/collection')
@login_required
def get_collection_images():
    form = SendCollectionForm()
    collection = request.args.get('collection')
    collection_images = Image.query.join(Collection.images).filter(Collection.id == collection).all()
    col_query = Collection.query.filter_by(id=collection).first()
    image_count = len(collection_images)
    name = col_query.name
    return render_template('collection_images.html', form=form, image_names=collection_images,image_count=image_count,col_query=col_query, collection=collection, name=name, title='Collections')


@app.route('/pickcollection')
def select_collection():
    selected_image = request.args.get('image')
    users_collections = Collection.query.filter(Collection._users.any(id=current_user.id)).all()
    return render_template('add_to_collection.html', image=selected_image, collections=users_collections)


@app.route('/add_to_collection', methods=['GET', 'POST'])
def add_to_collection():
    selected_image = request.args.get('image')
    selected_collection = request.args.get('collection')
    image_to_add = Image.query.filter_by(id=selected_image).first()
    chosen_collection = Collection.query.filter_by(id=selected_collection).first()
    chosen_collection.images.append(image_to_add)
    db.session.add(chosen_collection)
    db.session.commit()
    return redirect(url_for('get_user_collections'))


@app.route('/remove_from_collection', methods=['GET', 'POST'])
def remove_image():
    selected_image = request.args.get('image')
    selected_collection = request.args.get('collection')
    image_to_remove = Image.query.filter_by(id=selected_image).first()
    chosen_collection = Collection.query.filter_by(id=selected_collection).first()
    chosen_collection.images.remove(image_to_remove)
    db.session.commit()
    print(chosen_collection.id)
    print(image_to_remove.id)
    return redirect(url_for('get_user_collections'))


@app.route('/team', methods=['GET', 'POST'])
def team():
    form = AddUserForm()
    user_team = Team.query.filter(Team.id==current_user.team).first()
    team_name = user_team.name
    users = User.query.filter(User.team == user_team.id).all()
    sites = Site.query.join(Team.subscriptions).filter(Team.id == current_user.team).all()
    return render_template('team.html', team=team_name, users=users, sites=sites,current_user=current_user, title='Team',form=form)


@app.route('/sendcollection/<int:collection_id>', methods=['GET', 'POST'])
def send_collection(collection_id):
    form = SendCollectionForm()
    if form.validate_on_submit():
        email = form.email.data
        form_collection = form.collection.data
        print(form_collection)
        #collection = Collection.query.filter_by(id=form_collection)
        collection = Collection.query.get(collection_id)
        user = User.query.filter(User.email == email.lower()).first()
        if user is None:
            flash('User added')
            return redirect( url_for('get_user_collections'))
        else:
            user.collections_backref.append(collection)
            collection.sent_count += 1
            db.session.commit()
            msg = Message('New Collection Available', sender='e.eddieflores@gmail.com', recipients=[email])
            the_link = url_for('get_collection_images', _external=True, collection=collection.id)
            msg.html = render_template('/sent-collection-email.html', link=the_link, message=form.message.data)
            mail.send(msg)
            flash('Message Sent')
            return redirect( url_for('get_user_collections'))
    return render_template('/send_collection_form.html', form=form)
    # TODO Check if the user exist in the DB
    # TODO if user exists add to users collections and notify
    # TODO if user does not exist - Allow to download and invite to sign up


@app.route('/collection/sender', methods=['GET', 'POST'])
def collectionsender():
    collection = request.args.get('collection')
    email = request.args.get('email')
    collection = Collection.query.get(collection)
    user = User.query.filter(User.email == email.lower()).first()
    if user is None:
        flash('User added')
        return redirect( url_for('get_user_collections'))
    else:
        user.collections_backref.append(collection)
        msg = Message('New Collection Added', sender='e.eddieflores@gmail.com', recipients=[email])
        the_link = url_for('get_dates', _external=True, site='google.com')
        msg.html = render_template('/email-confirmation.html', link=the_link)
        mail.send(msg)
        return redirect(url_for('get_user_collections'))


@app.route('/deletecollection/<collection>', methods=['GET', 'POST'])
def delete_collection(collection):
    collection_to_remove = Collection.query.get(collection)
    current_user.collections_backref.remove(collection_to_remove)
    db.session.commit()
    # print('collection removed')
    flash('Collection removed', category='alert-info')
    return redirect(url_for('get_user_collections'))


# noinspection PyArgumentList
@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        # send the confirmation email
        email = form.email.data
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email', sender='e.eddieflores@gmail.com', recipients=[email])
        the_link = url_for('confirm_email', token=token, _external=True)
        msg.html = render_template('/email-confirmation.html', link=the_link)
        mail.send(msg)
        # add the new user to the database
        new_user = User(first_name=form.first_name.data,
                        email=form.email.data,
                        last_name=form.last_name.data,
                        nickname=form.first_name.data+" "+form.last_name.data,
                        profile='Standard User',
                        status='Active',
                        date_joined=datetime.today(),
                        collection_count=0)
        db.session.add(new_user)
        ## addnew user to team
        team = Team.query.filter(Team.id==current_user.team).first()
        print(team)
        db.session.commit()
        new_person = User.query.filter(User.email==form.email.data).first()
        print(new_person.id)
        team.admin_user.append(new_person)
        db.session.commit()
        flash('User Added', category='success')
        return redirect(url_for('team'))
    return render_template('adduser.html', form=form)



    # TODO

# THE REGISTRAION PROCESS

# The page with the two buttons
@app.route('/signup1')
def signup1():
    user = {'nickname': 'Eddie'}
    return render_template('/signup1.html', user=user)

# The page if user seleceted  to find their team based on email address
@app.route('/findteam', methods=['GET', 'POST'])
def findteamform():
    #add the form for finding your team
    # import the find a team form
    user = current_user
    formi = FindTeamForm()
    if formi.validate_on_submit():
        #Add the portion if email found in database, send via email
        # else send them to a page that says their team doesn't exist
        return flask.errorhandler(404)
    return render_template('/findteam.html', form=formi, user=user)

@app.errorhandler(404)
def page_not_found(e):
    user = {'nickname': 'Eddie'}
    return render_template('/404.html',user=user), 404
