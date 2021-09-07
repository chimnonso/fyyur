#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

# import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
import logging
from logging import Formatter, FileHandler
from sqlalchemy.sql.expression import distinct, desc, asc
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from models import Show, Artist, Artist_Genre, Venue, Venue_Genre
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# class Venue_Genre(db.Model):
#   __tablename__ = 'venue_genres'
#   id = db.Column(db.Integer, primary_key=True)
#   venue_id = db.Column(db.Integer, db.ForeignKey("venue.id", ondelete="CASCADE"), nullable=False)
#   genre = db.Column(db.String(50), nullable=False)

#   def __repr__(self):
#     return f"<Venue_Genre venue_id:{self.venue_id} genre: {self.genre}>"


# class Venue(db.Model):
#     __tablename__ = 'venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     address = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.String(120), nullable=True)
#     image_link = db.Column(db.String(500), nullable=True, default="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
#     facebook_link = db.Column(db.String(120), nullable=True)
#     genres = db.relationship("Venue_Genre", backref="venue", lazy=True)
#     website = db.Column(db.String(120), nullable=True)
#     seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
#     seeking_description = db.Column(db.String(200), nullable=True)
#     created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())


# class Show(db.Model):
#   __tablename__ = 'shows'
#   id = db.Column(db.Integer, primary_key=True)
#   venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
#   artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
#   start_time = db.Column(db.DateTime, nullable=False)

  
# class Artist_Genre(db.Model):
#   __tablename__ = 'artist_genres'
#   id = db.Column(db.Integer, primary_key=True)
#   artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
#   genre = db.Column(db.String(50), nullable=False)

#   def __repr__(self):
#     return f"<Artist_Genre artist_id:{self.artist_id} genre: {self.genre}>"


# class Artist(db.Model):
#     __tablename__ = 'artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.String(120), nullable=False)
#     image_link = db.Column(db.String(500), nullable=True, default="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
#     facebook_link = db.Column(db.String(120), nullable=True)
#     website = db.Column(db.String(120), nullable=True)
#     genres = db.relationship("Artist_Genre", backref="artist", lazy=True)
#     seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
#     seeking_description = db.Column(db.String(200), nullable=True)
#     # products = db.relationship('Product', secondary=order_items, backref=db.backref('orders', lazy=True))
#     venues = db.relationship("Venue", secondary="shows", backref=db.backref('artist', lazy=True))
#     created_on = db.Column(db.DateTime, nullable=False, default=datetime.now())





#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.parse(value)
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  fields = ['id', 'name', 'created_on']
  artists = Artist.query.options(load_only(*fields)).order_by(desc(Artist.created_on)).all()[:10]
  venues = Venue.query.options(load_only(*fields)).order_by(desc(Venue.created_on)).all()[:10]
  return render_template('pages/home.html', artists=artists, venues=venues)
  # return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  response_data = []
  locations = db.session.query(distinct(Venue.city), Venue.state).all()
  cur_time = datetime.now()
  
  for location in locations:
    city, state = location[0], location[1]

    venues = db.session.query(Venue).filter_by(city=city, state=state).all()
    data = {'city': city, 'state': state, "venues": []}

    for venue in venues:
      venue_data = {
        'id': venue.id,
        'name': venue.name,
      }

      # upcoming_shows = Show.query.filter_by(venue_id=venue_data['venue_id']).filter(Show.start_time > cur_time).all()
      # venue_data['num_upcoming_shows'] = len(upcoming_shows)

      data['venues'].append(venue_data)
    response_data.append(data)


  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  return render_template('pages/venues.html', areas=response_data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_query = request.form.get('search_term', "")
  search_response = {'count': 0, 'data': []}
  search_results = Venue.query.filter(Venue.name.ilike(f"%{search_query}%")).all()
  print(search_results)
  search_response['count'] = len(search_results)

  for result in search_results:
    item = {
      "id": result.id,
      'name': result.name
    }
    search_response['data'].append(item)
  return render_template('pages/search_venues.html', results=search_response, search_term=search_query)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id

  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue.id)
  cur_time = datetime.now()

  supposed_upcoming_shows = shows.filter(Show.start_time > cur_time).all()
  upcoming_shows = []

  for show in supposed_upcoming_shows:
    artist = Artist.query.get(show.artist_id)
    temp = {
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.start_time)
      } 
    upcoming_shows.append(temp)

  supposed_past_shows = shows.filter(Show.start_time < cur_time).all()
  past_shows = []
  
  for show in supposed_past_shows:
    artist = Artist.query.get(show.artist_id)
    temp = {
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.start_time)
      } 
    past_shows.append(temp)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "upcoming_shows": upcoming_shows,
    "past_shows": past_shows,
    "upcoming_shows_count": len(upcoming_shows),
    "past_shows_count": len(past_shows)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    phone = request.form.get("phone")
    genres = request.form.getlist("genres")
    facebook_link = request.form.get("facebook_link", "")
    image_link = request.form.get("image_link")
    website = request.form.get("website_link", "")
    seeking_talent = request.form.get("seeking_talent")
    seeking_description = request.form.get("seeking_description", "")
    print(genres)

    if seeking_talent == 'y':
      seeking_talent = True
    else:
      seeking_talent = False
    

    new_venue = Venue(name=name,
      city=city,
      state=state,
      address=address,
      phone=phone,
      facebook_link=facebook_link,
      # image_link=image_link,
      website=website,
      seeking_talent=seeking_talent,
      seeking_description=seeking_description)
    # new_venue = Venue(name="Eko Hotels",city="wuse",state="Abuja",address="14 apala",phone="456878",facebook_link="", image_link="", website="", seeking_talent=True, seeking_description="description")

    for genre in genres:
      current_genre = Venue_Genre(genre=genre)
      current_genre.venue = new_venue

    db.session.add(new_venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('index'))
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash("Venue  successfully deleted!")
  except:
    db.session.rollback()
    flash("Delete unsuccessful for Venue")
  finally:
    db.session.close()
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  fields = ['id', 'name']
  artists = Artist.query.options(load_only(*fields)).all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get("search_term", "")
  search_response = {'count': 0, 'data':[]}
  search_results = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
  search_response['count'] = len(search_results)
  for result in search_results:
    item = {
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(Show.query.filter_by(artist_id=result.id).all())
    }
    search_response["data"].append(item)
  
  return render_template('pages/search_artists.html', results=search_response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id

  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id)
  cur_time = datetime.now()
  supposed_past_shows = shows.filter(Show.start_time < cur_time).all()
  supposed_upcoming_shows = shows.filter(Show.start_time > cur_time).all()
  upcoming_shows = []
  past_shows = []

  for show in supposed_past_shows:
    venue = Venue.query.get(show.venue_id)
    temp = {
      'venue_id': venue.id,
      'venue_name': venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time)
    }
    past_shows.append(temp)

  for show in supposed_upcoming_shows:
    venue = Venue.query.get(show.venue_id)
    temp = {
      'venue_id': venue.id,
      'venue_name': venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time)
    }
    upcoming_shows.append(temp)
  genres = []
  for item in artist.genres:
    genres.append(item.genre)
  

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  try:
    artist = Artist.query.get(artist_id)
    if artist is None:
      return not_found_error(404)

    genres = []

    if len(artist.genres) > 0:
      for item in artist.genres:
        genres.append(item.genre)

    data = {
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link
    }

  except:
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    
    name  = request.form.get("name")
    genres  = request.form.getlist("genres")
    city  = request.form.get("city")
    state  = request.form.get("state")
    phone  = request.form.get("phone")
    website  = request.form.get("website")
    facebook_link  = request.form.get("facebook_link")
    seeking_venue  = request.form.get("seeking_venue")
    seeking_description  = request.form.get("seeking_description")
    image_link  = request.form.get("image_link")

         
    artist.name = name
    artist.city = city
    artist.state = state
    artist.phone = phone
    artist.website = website
    artist.facebook_link = facebook_link
    if seeking_venue == 'y':
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False
    artist.seeking_description = seeking_description 
    artist.image_link = image_link

    artist_genres = []
    for genre in genres:
      current_genre = Artist_Genre(genre=genre)
      current_genre.artist = artist
      artist_genres.append(current_genre)
    
    db.session.add(artist)
    db.session.commit()
    flash("Successfully update this artist")


  except:
    db.session.rollback()
    flash("Something went wrong while trying to update this artist")
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  try:
    venue = Venue.query.get(venue_id)
    if venue is None:
      return not_found_error(404)

    genres = []

    if len(venue.genres) > 0:
      for item in venue.genres:
        genres.append(item.genre)

    data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link
    }

  except:
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)

    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")
    address = request.form.get("address")
    phone = request.form.get("phone")
    image_link = request.form.get("image_link")
    facebook_link = request.form.get("facebook_link")
    genres = request.form.getlist("genres")
    website = request.form.get("website")
    seeking_talent = request.form.get("seeking_talent")
    seeking_description = request.form.get("seeking_description")
    print(seeking_talent)

    if seeking_talent == 'y':
      seeking_talent = True
    else:
      seeking_talent = False

    venue.name = name
    venue.city = city
    venue.state = state
    venue.address = address
    venue.phone = phone
    venue.image_link = image_link 
    venue.facebook_link = facebook_link
    venue.website = website
    venue.seeking_talent = seeking_talent
    venue.seeking_description = seeking_description

    for genre in genres:
      current_genre = Venue_Genre(genre=genre)
      current_genre.venue = venue

    db.session.add(venue)
    db.session.commit()
    flash("Successfully update this venue")


  except:
    db.session.rollback()
    flash("Something went wrong while updating venue")
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")
    phone = request.form.get("phone")
    image_link = request.form.get("image_link")
    facebook_link = request.form.get("facebook_link")
    website = request.form.get("website")
    genres = request.form.getlist("genres")
    seeking_venue = request.form.get("seeking_venue")
    seeking_description = request.form.get("seeking_description")

    if seeking_venue == 'y':
      seeking_venue = True
    else:
      seeking_venue = False

    new_artist = Artist(
      name = name, city = city, state = state,
      phone = phone, facebook_link = facebook_link,
      website = website, seeking_venue = seeking_venue,
      seeking_description = seeking_description
    )

    for genre in genres:
      current_genre = Artist_Genre(genre=genre)
      current_genre.artist = new_artist

    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('index'))

  except:
    db.session.rollback()
    flash("Something went wrong. Artist not added")
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  complete_show_data = []
  all_shows = Show.query.all()

  for show in all_shows:
    venue_id = show.venue_id
    artist_id = show.artist_id
    artist = Artist.query.get(artist_id)
    venue_name = Venue.query.get(venue_id).name
    start_time = str(show.start_time)

    data = {
      "venue_id":venue_id,
      "venue_name" : venue_name,
      "artist_id": artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": start_time
    }

    complete_show_data.append(data)
  return render_template('pages/shows.html', shows=complete_show_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  errors = {'no_artist': False, 'no_venue': False}

  try:
    print("artist_id")
    artist_id = request.form.get('artist_id')
    print(artist_id)
    venue_id = request.form.get('venue_id')
    start_time =  request.form.get('start_time')
    


    artist = Artist.query.get(artist_id)
    venue = Venue.query.get(venue_id)

    if artist is None:
      errors['no_venue'] = True
    
    if venue is None:
      errors['no_venue'] = True

    if artist is not None and venue is not None:
      new_show = Show(
        artist_id = artist_id,
        venue_id = venue_id,
        start_time = start_time
      )

      db.session.add(new_show)
      db.session.commit()
      flash(f"The show by {artist.name}, will hold at {venue.name}")
      return redirect(url_for('index'))
  except:
    print(sys.exc_info)
    db.session.rollback()
    flash("Seems the show was not created. Please try again")
  finally:
    db.session.close()

  if errors["no_artist"] is True:
    flash(f"Artist with id {artist_id} not found")
  if errors["no_venue"] is True:
    flash(f"Venue with id {venue_id} not found")
  return render_template('pages/home.html')



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
