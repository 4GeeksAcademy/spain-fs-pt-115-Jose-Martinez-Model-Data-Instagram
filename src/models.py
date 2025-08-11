import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

followers_table = Table(
    'followers',
    db.metadata,
    db.Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', Integer, ForeignKey('user.id'), primary_key=True)
)


class MediaType(enum.Enum):
    IMAGE = 'image'
    VIDEO = 'video'


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)

    # Relaciones bidireccionales
    posts: Mapped[list["Post"]] = relationship(back_populates='user')
    comments: Mapped[list["Comment"]] = relationship(back_populates='user')

    # a quién sigue este usuario.
    following: Mapped[list["User"]] = relationship(
        secondary=followers_table,
        primaryjoin=(followers_table.c.follower_id == id),
        secondaryjoin=(followers_table.c.followed_id == id),
        back_populates='followers'
    )
    # quiénes siguen a este usuario.
    followers: Mapped[list["User"]] = relationship(
        secondary=followers_table,
        primaryjoin=(followers_table.c.followed_id == id),
        secondaryjoin=(followers_table.c.follower_id == id),
        back_populates='following'
    )


class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    # nombres en minúscula, como es la convención.
    user: Mapped["User"] = relationship(back_populates='posts')
    comments: Mapped[list["Comment"]] = relationship(back_populates='post')
    media: Mapped[list["Media"]] = relationship(back_populates='post')


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(db.Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    post: Mapped["Post"] = relationship(back_populates='media')


class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    user: Mapped["User"] = relationship(back_populates='comments')
    post: Mapped["Post"] = relationship(back_populates='comments')
