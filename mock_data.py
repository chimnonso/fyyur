from app import Artist_Genre, Venue, Venue_Genre, Artist, Show
from faker import Faker
import random

fake = Faker()

try:
    from app import db
except:
    from __main__ import db

def insert_record(record):
    try:
        new_venue = Venue(
            name = record['name'],
            address = record['address'],
            city = record['city'],
            state = record['state'],
            phone = record['phone'],
            facebook_link = record['facebook_link'],
            seeking_talent = record['seeking_talent'],
            seeking_description = record['seeking_description'],
            image_link = record['image_link'],
            website = record['website']
        )
        for genre in record['genres']:
            current_genre = Venue_Genre(genre=genre)
            current_genre.venue = new_venue

        db.session.add(new_venue)
        db.session.commit()
        print("SUccessfull")
        return {'Venue insert successfully': True}
    except:
        db.session.rollback()
        return {'Venue insert unsuccessfully': False}
    finally:
        db.session.close()



def load_record():
    records = [{
            "name": "The Musical Hop",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            "address": "1015 Folsom Street",
            "city": "San Francisco",
            "state": "CA",
            "phone": "123-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        },{
            "name": "The Dueling Pianos Bar",
            "genres": ["Classical", "R&B", "Hip-Hop"],
            "address": "335 Delancey Street",
            "city": "New York",
            "state": "NY",
            "phone": "914-003-1132",
            "website": "https://www.theduelingpianos.com",
            "facebook_link": "https://www.facebook.com/theduelingpianos",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        },{
            "name": "Park Square Live Music & Coffee",
            "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
            "address": "34 Whiskey Moore Ave",
            "city": "San Francisco",
            "state": "CA",
            "phone": "415-000-1234",
            "website": "https://www.parksquarelivemusicandcoffee.com",
            "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        },{
            "name": "Back Street Boiz",
            "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
            "address": "34 Whiskey Moore Ave",
            "city": "Texas",
            "state": "CA",
            "phone": "415-000-1234",
            "website": "https://www.backstreetboiz.com",
            "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        },{
            "name": "Westlife",
            "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
            "address": "34 Whiskey Moore Ave",
            "city": "San Francisco",
            "state": "CA",
            "phone": "415-000-1234",
            "website": "https://westlife.com",
            "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        }]

    return records

records = load_record()

for record in records:
    insert_record(record)





genres = ["Jazz", "Reggae", "Swing", "Classical", "Folk", "Rock n Roll", "Folk", "R&B", "Hip-Hop"]
def insert_artist():
  
    artist_genres = random.sample(genres, 4)
    try:
        new_artist = Artist(
            name = fake.name(),
            phone = fake.phone_number(),
            city = fake.city(),
            state = fake.state(),
            seeking_description = fake.text(),
            website = fake.domain_name()
        )
            
        for genre in artist_genres:
            current_genre = Artist_Genre(genre=genre)
            current_genre.artist = new_artist

        print("adding artist..")
        db.session.add(new_artist)
        db.session.commit()
        print("added .....")
        return {'Artist insert successfully': True}
    except:
        db.session.rollback()
        return {'Artist insert unsuccessfully': False}
    finally:
        db.session.close()

# load_record()

# for i in range(10):
#     insert_artist()


