from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
""" from __future__ import annotations """
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    lastname: Mapped[str] =  mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    followers: Mapped[List["Follower"]] = relationship(
        back_populates="user")
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
        
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[enumerate] = mapped_column()
    url: Mapped[str] = mapped_column(nullable=False)
    post_id:


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
