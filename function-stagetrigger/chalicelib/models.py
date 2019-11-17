from sqlalchemy import Column, DateTime, ForeignKey, String, text as lit
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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
    

class Person(Base):
    __tablename__ = 'person'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11))
    first_name = Column(String(64))
    last_name = Column(String(64))
    

class Post(Base):
    __tablename__ = 'post'

    id = Column(INTEGER(11), primary_key=True)
    chat_id = Column(ForeignKey('chat.id'), index=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    person_id = Column(ForeignKey('person.id'), index=True)
    text = Column(String(1024), nullable=False)
    date_added = Column(DateTime, nullable=False)

    chat = relationship('Chat')
    path = relationship('Path')
    person = relationship('Person')


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
    
    path = relationship('Path')


class AlbumTrack(Base):
    __tablename__ = 'album_tracks'

    id = Column(INTEGER(11), primary_key=True)
    album_id = Column(ForeignKey('album.id'), index=True)
    track_id = Column(ForeignKey('track.id'), index=True)

    album = relationship('Album')
    track = relationship('Track')


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(INTEGER(11), primary_key=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    name = Column(String(256))

    path = relationship('Path')


class AlbumArtist(Base):
    __tablename__ = 'album_artists'

    id = Column(INTEGER(11), primary_key=True)
    album_id = Column(ForeignKey('album.id'), index=True)
    artist_id = Column(ForeignKey('artist.id'), index=True)

    artist = relationship('Artist')
    album = relationship('Album')


class ArtistGenre(Base):
    __tablename__ = 'artist_genres'

    id = Column(INTEGER(11), primary_key=True)
    artist_id = Column(ForeignKey('artist.id'), index=True)
    genre_id = Column(ForeignKey('genre.id'), index=True)


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String)


class Path(Base):
    __tablename__ = 'path'

    id = Column(INTEGER(11), primary_key=True)
    type = Column(String(48))
    uri = Column(String(512))
    platform = Column(String(45))
    

class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(INTEGER(11), primary_key=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    title = Column(String(256))

    path = relationship('Path')


class PlaylistTrack(Base):
    __tablename__ = 'playlist_tracks'

    id = Column(INTEGER(11), primary_key=True)
    playlist_id = Column(ForeignKey('playlist.id'), index=True)
    track_id = Column(ForeignKey('track.id'), index=True)

    playlist = relationship('Playlist')
    track = relationship('Track')


class Track(Base):
    __tablename__ = 'track'

    id = Column(INTEGER(11), primary_key=True)
    path_id = Column(ForeignKey('path.id'), index=True)
    title = Column(String(256))

    path = relationship('Path')


class TrackArtist(Base):
    __tablename__ = 'track_artists'

    id = Column(INTEGER(11), primary_key=True)
    track_id = Column(ForeignKey('track.id'), index=True)
    artist_id = Column(ForeignKey('artist.id'), index=True)

    artist = relationship('Artist')
    track = relationship('Track')
