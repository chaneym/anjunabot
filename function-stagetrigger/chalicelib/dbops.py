import os
import chalicelib.spotify as sp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chalicelib import models as m

DB_CON_STRING = os.environ['DB_CON_STRING']

write_engine = create_engine(DB_CON_STRING)
WriteSession = sessionmaker(bind=write_engine)


def session_manager():
    return WriteSession()


def get_or_create(session, model, **kwargs):

    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance


def commit_or_rollback(session):
    try:
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()


def get_row_by_id(model, row_id):
    session = WriteSession()
    instance = session.query(model).filter_by(id=row_id).first()
    if instance:
        return instance


def insert_track_artists_genres(session, track_dict, album, track_artists, platform):
    track = get_or_create(session, m.Track, **track_dict)

    for artist_json in track_artists:
        artist_path_dict = {'type': 'artist', 'uri': artist_json['id'], 'platform': platform}
        artist_path = get_or_create(session, m.Path, **artist_path_dict)
        artist_dict = {'path_id': artist_path.id, 'name': artist_json['name']}
        artist = get_or_create(session, m.Artist, **artist_dict)

        track_artist_dict = {'track_id': track.id, 'artist_id': artist.id}
        get_or_create(session, m.TrackArtist, **track_artist_dict)

        if album:
            album_artist_dict = {'album_id': album.id, 'artist_id': artist.id}
            get_or_create(session, m.AlbumArtist, **album_artist_dict)

        media_json = sp.get_artist_info(artist_json['id'])
        for genre_name in media_json['genres']:
            genre_dict = {'name': genre_name}
            genre = get_or_create(session, m.Genre, **genre_dict)

            artist_genre_dict = {'artist_id': artist.id, 'genre_id': genre.id}
            get_or_create(session, m.ArtistGenre, **artist_genre_dict)

    return track

