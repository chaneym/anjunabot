from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# metadata = Base.metadata


'''
Staging Tables
'''


class MessageStage(Base):
    __tablename__ = 'message_stage'

    id = Column(INTEGER(11), primary_key=True)
    path = Column(String(512), nullable=False)
    user_id = Column(INTEGER(11))
    path_type = Column(String(48))
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64))
    text = Column(String(1024), nullable=False)
    chat_id = Column(INTEGER(11), nullable=False)
    chat_title = Column(String(128), nullable=False)
    platform = Column(String(48), nullable=False)
    transformed = Column(INTEGER(11), nullable=False)
    

'''
Telegram Meta Data Tables
'''


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(INTEGER(11), primary_key=True)
    cid = Column(INTEGER(11))
    title = Column(String(128))

    posts = relationship('Post', back_populates='chat')
    

class Person(Base):
    __tablename__ = 'person'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11))
    first_name = Column(String(64))
    last_name = Column(String(64))

    posts = relationship('Post', back_populates='person')
    

class Post(Base):
    __tablename__ = 'post'

    id = Column(INTEGER(11), primary_key=True)
    chat_id = Column(ForeignKey('chat.id'), index=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    person_id = Column(ForeignKey('person.id'), index=True)
    text = Column(String(1024), nullable=False)

    chat = relationship('Chat', back_populates='posts')
    path = relationship('Path', back_populates='posts')
    person = relationship('Person', back_populates='posts')


'''
Media Metadata Tables
'''


class Album(Base):
    __tablename__ = 'album'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(256))
    type = Column(String(64))
    num_tracks = Column(INTEGER(11))
    path_id = Column(ForeignKey('path.id'), index=True)
    
    path = relationship('Path', uselist=False, back_populates='album')
    artists = relationship('Artist', secondary='album_artists', back_populates='albums')
    tracks = relationship('Track', secondary='album_tracks', back_populates='albums')


class AlbumTrack(Base):
    __tablename__ = 'album_tracks'

    id = Column(INTEGER(11), primary_key=True)
    album_id = Column(ForeignKey('album.id'), index=True)
    track_id = Column(ForeignKey('track.id'), index=True)


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(INTEGER(11), primary_key=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    name = Column(String(256))

    path = relationship('Path', uselist=False, back_populates='artist')
    albums = relationship('Album', secondary='album_artists', back_populates='artists')
    tracks = relationship('Track', secondary='track_artists', back_populates='artists')
    genres = relationship('Genre', secondary='artist_genres', back_populates='artists')


class AlbumArtist(Base):
    __tablename__ = 'album_artists'

    id = Column(INTEGER(11), primary_key=True)
    album_id = Column(ForeignKey('album.id'), index=True)
    artist_id = Column(ForeignKey('artist.id'), index=True)


class ArtistGenre(Base):
    __tablename__ = 'artist_genres'

    id = Column(INTEGER(11), primary_key=True)
    artist_id = Column(ForeignKey('artist.id'), index=True)
    genre_id = Column(ForeignKey('genre.id'), index=True)


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String)

    artists = relationship('Artist', secondary='artist_genres', back_populates='genres')


class Path(Base):
    __tablename__ = 'path'

    id = Column(INTEGER(11), primary_key=True)
    type = Column(String(48))
    uri = Column(String(512))
    platform = Column(String(45))

    album = relationship('Album', uselist=False, back_populates='path')
    artist = relationship('Artist', uselist=False, back_populates='path')
    track = relationship('Track', uselist=False, back_populates='path')
    playlist = relationship('Playlist', uselist=False, back_populates='path')
    posts = relationship('Post', back_populates='path')
    

class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(INTEGER(11), primary_key=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    title = Column(String(256))

    path = relationship('Path', uselist=False, back_populates='playlist')
    tracks = relationship('Track', secondary='playlist_tracks', back_populates='playlists')


class PlaylistTrack(Base):
    __tablename__ = 'playlist_tracks'

    id = Column(INTEGER(11), primary_key=True)
    playlist_id = Column(ForeignKey('playlist.id'), index=True)
    track_id = Column(ForeignKey('track.id'), index=True)


class Track(Base):
    __tablename__ = 'track'

    id = Column(INTEGER(11), primary_key=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    title = Column(String(256))

    path = relationship('Path', back_populates='track')
    albums = relationship('Album', secondary='album_tracks', back_populates='tracks')
    artists = relationship('Artist', secondary='track_artists', back_populates='tracks')
    playlists = relationship('Playlist', secondary='playlist_tracks', back_populates='tracks')


class TrackArtist(Base):
    __tablename__ = 'track_artists'

    id = Column(INTEGER(11), primary_key=True)
    track_id = Column(ForeignKey('track.id'), index=True)
    artist_id = Column(ForeignKey('artist.id'), index=True)

