from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)  # unique eliminado (corrección)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)   # unique eliminado (corrección)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Relación con los que este usuario sigue
    followers: Mapped[List["Follower"]] = relationship(
        back_populates="user", foreign_keys="Follower.user_from_id", cascade="all, delete-orphan"
    )

    # Relación con los usuarios que lo siguen
    followed: Mapped[List["Follower"]] = relationship(
        back_populates="target", foreign_keys="Follower.user_to_id", cascade="all, delete-orphan"
    )

    # Relación con los posts creados por este usuario
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    # Relación con los comentarios escritos por este usuario
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    # Usuario que sigue a otro
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relaciones inversas para acceder a los datos completos del seguidor y seguido
    user: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[user_from_id])
    target: Mapped["User"] = relationship(back_populates="followed", foreign_keys=[user_to_id])

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relación con el usuario que creó el post
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")

    # Relación con los comentarios asociados al post
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )

    # Relación con los medios (fotos/videos) asociados al post
    media: Mapped[List["Media"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[str] = mapped_column(nullable=False)  # conservamos 'media_type' como solicitaste
    url: Mapped[str] = mapped_column(nullable=False)

    # Relación con el post al que pertenece este medio
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "media_type": self.media_type,
            "url": self.url,
            "post_id": self.post_id
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)

    # Relación con el usuario que escribió el comentario
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="comments")

    # Relación con el post al que se hizo el comentario
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
