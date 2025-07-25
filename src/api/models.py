from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text, Boolean, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    lastname: Mapped[str] = mapped_column(Text, nullable=False)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    country: Mapped[str] = mapped_column(String(120), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    user_bases: Mapped[list["Base"]] = relationship("Base", back_populates="bases_user", cascade="all, delete-orphan")
    user_missions: Mapped[list["UserMission"]] = relationship("UserMission", back_populates="missions_user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "username": self.username,
            "image": self.image,
            "email": self.email,
            "city": self.city,
            "country": self.country,
            "rol": self.rol
            # do not serialize the password, its a security breach
        }
        
class Base(db.Model):
    __tablename__ = "base"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    base: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[str] = mapped_column(String(50), nullable=False)
    longitude: Mapped[str] = mapped_column(String(50), nullable=False)
    
    bases_user: Mapped["User"] = relationship("User", back_populates="user_bases")
    base_missions: Mapped[list["UserMission"]] = relationship("UserMission", back_populates="missions_base")
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "base": self.base,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
    
class Event(db.Model):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    event: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    moon: Mapped[str] = mapped_column(String(100), nullable=False)
    visibility: Mapped[str] = mapped_column(String(100), nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=False)
    
    event_missions: Mapped[list["UserMission"]] = relationship("UserMission", back_populates="missions_event")
    
    def serialize(self):
        return{
            "id": self.id,
            "event": self.event,
            "category": self.category,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "moon": self.moon,
            "visibility": self.visibility,
            "image": self.image
        }
        
class UserMission(db.Model):
    __tablename__ = "user_mission"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    base_id: Mapped[int] = mapped_column(ForeignKey("base.id", ondelete="CASCADE"), nullable=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id", ondelete="CASCADE"))
    state: Mapped[str] = mapped_column(String(15), nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=True)
    done_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    missions_user: Mapped["User"] = relationship("User", back_populates="user_missions")
    missions_base: Mapped["Base"] = relationship("Base", back_populates="base_missions")
    missions_event: Mapped["Event"] = relationship("Event", back_populates="event_missions")
    
    def serialize(self):
        return{
            "id": self.id,
            "user": {
                "id": self.user_id,
                "name": self.missions_user.name if self.missions_user else None,
                "lastname": self.missions_user.lastname if self.missions_user else None,
                "username": self.missions_user.username if self.missions_user else None,
                "image": self.missions_user.image if self.missions_user else None,
                "email": self.missions_user.email if self.missions_user else None,
                "city": self.missions_user.city if self.missions_user else None,
                "country": self.missions_user.country if self.missions_user else None,
                "is_active": self.missions_user.is_active if self.missions_user else None,
            },
            "base": {
                "id": self.base_id,
                "base_name": self.missions_base.base if self.missions_base else None,  
                "latitude": self.missions_base.latitude if self.missions_base else None,
                "longitude": self.missions_base.longitude if self.missions_base else None
            },
            "event": {
                "id": self.event_id,
                "name": self.missions_event.event if self.missions_event else None,
                "category": self.missions_event.category if self.missions_event else None,
                "start_date": self.missions_event.start_date if self.missions_event else None,
                "end_date": self.missions_event.end_date if self.missions_event else None,
                "moon": self.missions_event.moon if self.missions_event else None,
                "visibility": self.missions_event.visibility if self.missions_event else None,
            },
            "state": self.state,
            "image": self.image,
            "done_date": self.done_date
        }