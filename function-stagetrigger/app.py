import os
import json
import chalicelib.models as m
from chalicelib import dbops
from chalicelib import spotify
from chalice import Chalice

ENV_NAME = os.getenv('ENV_NAME')
app = Chalice(app_name='stagetrigger-{env}'.format(env=ENV_NAME))


@app.on_sns_message(topic='topic-dbstage-{env}'.format(env=ENV_NAME))
def lambda_handler(event):
    session = dbops.session_manager()

    if os.getenv('AWS_REGION') is not None:
        row_id = json.loads(event.message)['row_id']
    else:
        row_id = event['row_id']

    ms = dbops.get_row_by_id(m.MessageStage, row_id)
    if ms.transformed == 1:
        return

    person_dict = {'first_name': ms.first_name, 'last_name': ms.last_name, 'user_id': ms.user_id}
    person = dbops.get_or_create(session, m.Person, **person_dict)

    chat_dict = {'cid': ms.chat_id, 'title': ms.chat_title}
    chat = dbops.get_or_create(session, m.Chat, **chat_dict)

    path_dict = {'type': ms.path_type, 'uri': ms.path, 'platform': ms.platform}
    path = dbops.get_or_create(session, m.Path, **path_dict)

    post_dict = {'chat_id': chat.id, 'path_id': path.id, 'person_id': person.id, 'text': ms.text}
    dbops.get_or_create(session, m.Post, **post_dict)

    if ms.platform == 'spotify':

        if ms.path_type == 'track':
            media_json = spotify.get_track_info(ms.path)

            album_path_dict = {'type': 'album', 'uri': media_json['album']['id'], 'platform': ms.platform}
            album_path = dbops.get_or_create(session, m.Path, **album_path_dict)
            album_dict = {'path_id': album_path.id, 'title': media_json['album']['name'], 'type': media_json['album']['album_type'],
                          'num_tracks': media_json['album']['total_tracks']}
            album = dbops.get_or_create(session, m.Album, **album_dict)

            track_dict = {'path_id': path.id, 'title': media_json['name']}
            track = dbops.insert_track_artists_genres(session, track_dict, album, media_json['artists'], ms.platform)

            album_track_dict = {'album_id': album.id, 'track_id': track.id}
            dbops.get_or_create(session, m.AlbumTrack, **album_track_dict)

            ms.transformed = 1

        if ms.path_type == 'album':
            media_json = spotify.get_album_info(ms.path)

            album_dict = {'path_id': path.id, 'title': media_json['name'], 'type': media_json['album_type'],
                          'num_tracks': media_json['total_tracks']}
            album = dbops.get_or_create(session, m.Album, **album_dict)

            for artist in media_json['artists']:
                artist_path_dict = {'type': 'artist', 'uri': artist['id'], 'platform': ms.platform}
                artist_path = dbops.get_or_create(session, m.Path, **artist_path_dict)
                artist_dict = {'path_id': artist_path.id, 'name': artist['name']}
                artist = dbops.get_or_create(session, m.Artist, **artist_dict)

                album_artist_dict = {'album_id': album.id, 'artist_id': artist.id}
                dbops.get_or_create(session, m.AlbumArtist, **album_artist_dict)

            for track in media_json['tracks']['items']:
                track_path_dict = {'type': 'track', 'uri': track['id'], 'platform': ms.platform}
                track_path = dbops.get_or_create(session, m.Path, **track_path_dict)
                track_dict = {'path_id': track_path.id, 'title': track['name']}
                track = dbops.insert_track_artists_genres(session, track_dict, album, track['artists'], ms.platform)

                album_track_dict = {'album_id': album.id, 'track_id': track.id}
                dbops.get_or_create(session, m.AlbumTrack, **album_track_dict)

            ms.transformed = 1

        if ms.path_type == 'artist':
            media_json = spotify.get_artist_info(ms.path)

            artist_dict = {'path_id': path.id, 'name': media_json['name']}
            artist = dbops.get_or_create(session, m.Artist, **artist_dict)

            for genre_name in media_json['genres']:
                genre_dict = {'name': genre_name}
                genre = dbops.get_or_create(session, m.Genre, **genre_dict)

                artist_genre_dict = {'artist_id': artist.id, 'genre_id': genre.id}
                dbops.get_or_create(session, m.ArtistGenre, **artist_genre_dict)

            ms.transformed = 1

        if ms.path_type == 'playlist':
            media_json = spotify.get_playlist_info(ms.path)

            playlist_dict = {'path_id': path.id, 'title': media_json['name']}
            playlist = dbops.get_or_create(session, m.Playlist, **playlist_dict)

            for track in media_json['tracks']['items']:
                track_path_dict = {'type': 'track', 'uri': track['track']['id'], 'platform': ms.platform}
                track_path = dbops.get_or_create(session, m.Path, **track_path_dict)
                track_dict = {'path_id': track_path.id, 'title': track['track']['name']}
                track = dbops.insert_track_artists_genres(session, track_dict, None, track['track']['artists'], ms.platform)

                playlist_track_dict = {'playlist_id': playlist.id, 'track_id': track.id}
                dbops.get_or_create(session, m.PlaylistTrack, **playlist_track_dict)

            ms.transformed = 1

    dbops.commit_or_rollback(session)
