from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['UPLOADED_IMAGES_DEST'] = '/static/media'
debug = DebugToolbarExtension(app)
images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Renders home page with pets"""
    pets = Pet.query.order_by(Pet.available.desc(), Pet.name.asc()).all()

    return render_template('index.html', pets=pets)


@app.route('/<int:pid>')
def show_pet_info(pid):
    """Renders page with pets information, using its db id"""
    pet = Pet.query.get(pid)

    return render_template('pet.html', pet=pet)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Renders pet form and handles adding new pet to db"""
    form = PetForm()

    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('static/media/' + filename)
        # kwargs = {k: v for k, v in form.data.items() if k != "csrf_token"}
        # new_pet = Pet(**kwargs)
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            age=form.age.data,
            notes=form.notes.data,
            available=form.available.data
        )
        if form.photo.data:
            new_pet.photo = 'static/media/' + f'{form.photo.data.filename}'
        elif form.photo_url.data:
            new_pet.photo_url = form.photo_url.data
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Created new pet: {new_pet.name}", 'success')
        return redirect('/')
    else:
        return render_template("add_pet_form.html", form=form)


@app.route('/<int:pid>/edit', methods=["GET", "POST"])
def edit_pet(pid):
    """Renders pet form and handles populating fields and updating db"""
    pet = Pet.query.get_or_404(pid)
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data if form.photo_url else pet.photo_url
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash(f"Edited pet: {pet.name}", 'success')
        return redirect(f'/{pid}')
    else:
        return render_template("edit_pet_form.html", form=form)
