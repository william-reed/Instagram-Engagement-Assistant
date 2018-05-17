from sqlalchemy import Column, BigInteger, DateTime, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime
import enum

Base = declarative_base()

# an instagram account
class Instagram_User(Base):
	__tablename__ = 'instagram_user'

	instagram_user_id = Column(BigInteger, primary_key=True)
	timestamp = Column(DateTime, default=datetime.datetime.utcnow)
	username = Column(String(length=256), nullable=False)
	followers = Column(Integer, nullable=False)
	following  = Column(Integer, nullable=False)
	is_business = Column(Boolean, nullable=False)
	is_private = Column(Boolean, nullable=False)

	scanned_by = relationship("Scan", back_populates="scanned_user",
		foreign_keys="Scan.instagram_user_id")
	initiated_scans = relationship("Scan", back_populates="initiating_user",
		foreign_keys="Scan.initiated_by")
	media = relationship("Media", back_populates="instagram_user")
	comments = relationship("Comment", back_populates="instagram_user")
	caused_interactions = relationship("Interaction", back_populates="interactor",
		foreign_keys="Interaction.interactor_id")
	been_interacted_by = relationship("Interaction", back_populates="interacted",
		foreign_keys="Interaction.interacted_id")

# representative of a particular scan or scraping instance
class Scan(Base):
	__tablename__ = 'scan'

	scan_id = Column(Integer, primary_key=True, autoincrement=True)
	# same as user_pk from instagram api; the user being scanned
	instagram_user_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"))
	timestamp = Column(DateTime, default=datetime.datetime.utcnow)
	# the client user that initiated this scan
	initiated_by = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"))

	scanned_user = relationship("Instagram_User", back_populates="scanned_by",
		foreign_keys="Scan.instagram_user_id")
	initiating_user = relationship("Instagram_User", back_populates="initiated_scans",
		foreign_keys="Scan.initiated_by")


# an instagram media entity (photo, video, etc)
class Media(Base):
	__tablename__ = 'media'

	media_id = Column(BigInteger, primary_key=True)
	instagram_user_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)
	is_picture = Column(Boolean)

	instagram_user = relationship("Instagram_User", back_populates="media")
	comments = relationship("Comment", back_populates="media")


# a users comment
class Comment(Base):
	__tablename__ = 'comment'

	comment_id = Column(BigInteger, primary_key=True)
	media_id = Column(BigInteger, ForeignKey("media.media_id"), nullable=False)
	instagram_user_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)
	text = Column(String(length=4096), nullable=False)
	# comment type. i think 0 is top level, and 2 is a reply
	type = Column(Integer, nullable=False)

	instagram_user = relationship("Instagram_User", back_populates="comments")
	media = relationship("Media", back_populates="comments")

# keep track of particular interaction types
class InteractionType(enum.Enum):
    follow = 0
    like = 1
    comment = 2

# a non automated user engagement
class Interaction(Base):
	__tablename__ = 'interaction'

	interaction_id = Column(Integer, primary_key=True, autoincrement=True)
	media_id = Column(BigInteger, ForeignKey("media.media_id"), nullable=False)
	interaction_type = Column(Enum(InteractionType), nullable=False)
	# the account interacted with
	interacted_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)
	# the account that created the interaction
	interactor_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)

	media = relationship("Media")
	interacted = relationship("Instagram_User", back_populates="been_interacted_by",
		foreign_keys="Interaction.interacted_id")
	interactor = relationship("Instagram_User", back_populates="caused_interactions",
		foreign_keys="Interaction.interactor_id")
