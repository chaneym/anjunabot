import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chalicelib.models import *

DB_CON_STRING = os.environ['DB_CON_STRING']

write_engine = create_engine(DB_CON_STRING)
WriteSession = sessionmaker(bind=write_engine)


def get_session():
    return WriteSession()


def get_message_row_by_id(session, row_id):
    instance = session.query(MessageStage).filter_by(id=row_id).first()
    if instance:
        return instance


def load_post(session, chat_dict, person_dict, path_dict, text):
    chat = load_dimension(session, Chat, **chat_dict)
    person = load_dimension(session, Person, **person_dict)
    path = load_dimension(session, Path, **path_dict)

    post = Post(text=text, chat=chat, person=person, path=path)

    session.add(post)
    session.commit()


def load_album(session, album_dict, path_dict, artist_dicts, track_dicts):
    if model_exists(session, Album, **album_dict):
        return False
    path = load_dimension(session, Path, **path_dict)
    album_dict['path'] = path

    album = Album(**album_dict)

    for track_dict in track_dicts:
        track = load_dimension(session, Track, **track_dict)
        album.tracks.append(track)

    for artist_dict in artist_dicts:
        artist = load_dimension(session, Artist, **artist_dict)
        album.artists.append(artist)

    session.add(album)
    session.commit()
    return True


def load_artist(session, artist_dict, path_dict, genre_dicts):
    if model_exists(session, Artist, **artist_dict):
        return False
    path = load_dimension(session, Path, **path_dict)
    artist_dict['path'] = path

    artist = Artist(**artist_dict)

    for genre_dict in genre_dicts:
        genre = load_dimension(session, Genre, **genre_dict)
        artist.genres.append(genre)

    session.add(artist)
    session.commit()
    return True


def load_track(session, path_dict, track_dict, artist_dicts, album_dict):
    if model_exists(session, Track, **track_dict):
        return False

    path = load_dimension(session, Path, **path_dict)
    track_dict['path'] = path

    track = Track(**track_dict)

    for album_dict in album_dict:
        album = load_dimension(session, Album, **album_dict)
        track.albums.append(album)
        for artist_dict in artist_dicts:
            artist = load_dimension(session, Artist, **artist_dict)
            album.artists(artist)
            track.artists.append(artist)

    session.add(track)
    session.commit()
    return True


def load_playlist(session, path_dict, playlist_dict, track_dicts):
    if model_exists(session, Playlist, **playlist_dict):
        return False

    path = load_dimension(session, Path, **path_dict)
    playlist_dict['path'] = path

    playlist = Playlist(**playlist_dict)

    for track_dict in track_dicts:
        track = load_dimension(session, Track, **track_dict)
        playlist.tracks.append(track)

    session.add(playlist)
    session.commit()
    return True
    

def load_path(session, path_dict):
    return load_dimension(session, Path, **path_dict)


def load_dimension(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance is None:
        instance_model = model(**kwargs)
        session.add(instance_model)
        return instance_model
    else:
        return instance


def model_exists(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance is None:
        return False
    else:
        return True
