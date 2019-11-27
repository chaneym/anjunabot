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


def load_album(session, path_dict, media_json, message):
    album_dict = {'title': media_json['name'], 'type': media_json['album_type'], 'num_tracks': media_json['total_tracks']}

    if model_exists(session, Album, **album_dict):
        return False

    path = load_dimension(session, Path, **path_dict)
    album_dict['path'] = path

    album = Album(**album_dict)

    # tracks with no artist associations
    for track_json in media_json['tracks']['items']:
        track_path_dict = {'type': 'track', 'uri': track_json['id'], 'platform': message.platform}
        track_path = load_path(session, track_path_dict)
        track_dict = {'title': track_json['name'], 'path': track_path}
        track = load_dimension(session, Track, **track_dict)
        for artist_json in track_json['artists']:
            artist_path_dict = {'type': 'artist', 'uri': artist_json['id'], 'platform': message.platform}
            artist_path = load_path(session, artist_path_dict)
            artist_dict = {'name': artist_json['name'], 'path': artist_path}
            artist = load_dimension(session, Artist, **artist_dict)
            track.artists.append(artist)

    for artist_json in media_json['artists']:
        artist_path_dict = {'type': 'artist', 'uri': artist_json['id'], 'platform': message.platform}
        artist_path = load_path(session, artist_path_dict)
        artist_dict = {'name': artist_json['name'], 'path': artist_path}
        artist = load_dimension(session, Artist, **artist_dict)

        album.artists.append(artist)

    session.add(album)
    session.commit()
    return True


def load_artist(session, path_dict, media_json):
    artist_dict = {'name': media_json['name']}
    if model_exists(session, Artist, **artist_dict):
        return False

    genre_dicts = []
    for genre_name in media_json['genres']:
        genre_dict = {'name': genre_name}
        genre_dicts.append(genre_dict)

    path = load_dimension(session, Path, **path_dict)
    artist_dict['path'] = path

    artist = Artist(**artist_dict)

    for genre_dict in genre_dicts:
        genre = load_dimension(session, Genre, **genre_dict)
        artist.genres.append(genre)

    session.add(artist)
    session.commit()
    return True


def load_track(session, path_dict, media_json, message):
    track_dict = {'title': media_json['name']}
    if model_exists(session, Track, **track_dict):
        return False

    path = load_dimension(session, Path, **path_dict)
    track_dict['path'] = path
    track = Track(**track_dict)

    album_path_dict = {'type': 'album', 'uri': media_json['album']['id'], 'platform': message.platform}
    album_path = load_path(session, album_path_dict)
    album_dict = {'path': album_path, 'title': media_json['album']['name'], 'type': media_json['album']['album_type'],
                  'num_tracks': media_json['album']['total_tracks']}
    album = load_dimension(session, Album, **album_dict)

    # find album artist associations
    for artist_json in media_json['album']['artists']:
        artist_path_dict = {'type': 'artist', 'uri': artist_json['id'], 'platform': message.platform}
        album_artist_path = load_path(session, artist_path_dict)
        album_artist_dict = {'path': album_artist_path, 'name': artist_json['name']}
        artist = load_dimension(session, Artist, **album_artist_dict)
        album.artists.append(artist)

    track.albums.append(album)

    for artist_json in media_json['artists']:
        artist_path_dict = {'type': 'artist', 'uri': artist_json['id'], 'platform': message.platform}
        artist_path = load_path(session, artist_path_dict)
        artist_dict = {'name': artist_json['name'], 'path': artist_path}
        artist = load_dimension(session, Artist, **artist_dict)
        track.artists.append(artist)

    session.add(track)
    session.add(album)
    session.commit()
    return True


def load_playlist(session, path_dict, media_json, message):
    playlist_dict = {'title': media_json['name']}

    if model_exists(session, Playlist, **playlist_dict):
        return False

    path = load_dimension(session, Path, **path_dict)
    playlist_dict['path'] = path

    playlist = Playlist(**playlist_dict)

    for track_json in media_json['tracks']['items']:
        track_json = track_json['track']
        track_path_dict = {'type': 'track', 'uri': track_json['id'], 'platform': message.platform}
        track_path = load_path(session, track_path_dict)
        track_dict = {'title': track_json['name'], 'path': track_path}
        track = load_dimension(session, Track, **track_dict)

        album_json = track_json['album']
        album_path_dict = {'type': 'album', 'uri': album_json['id'], 'platform': message.platform}
        album_path = load_path(session, album_path_dict)
        album_dict = {'title': album_json['name'], 'path': album_path, 'type': album_json['album_type'], 'num_tracks': album_json['total_tracks']}
        album = load_dimension(session, Album, **album_dict)
        # artists on the album
        for artist_json in album_json['artists']:
            artist_path_dict = {'type': 'artist', 'uri': artist_json['id'], 'platform': message.platform}
            artist_path = load_path(session, artist_path_dict)
            artist_dict = {'name': artist_json['name'], 'path': artist_path}
            artist = load_dimension(session, Artist, **artist_dict)
            album.artists.append(artist)

        track.albums.append(album)

        for artist_json in track_json['artists']:
            artist_path_dict = {'type': 'artist', 'uri': artist_json['id'], 'platform': message.platform}
            artist_path = load_path(session, artist_path_dict)
            artist_dict = {'name': artist_json['name'], 'path': artist_path}
            artist = load_dimension(session, Artist, **artist_dict)
            track.artists.append(artist)

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

