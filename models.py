from sqlalchemy import Column, BigInteger, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()

# representative of a particular scan or scraping instance
class Scan(Base):
	__tablename__ = 'scan'

	scan_id = Column(BigInteger, primary_key=True, autoincrement=True)
	# same as user_pk from instagram api
	instagram_user_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"))
	timestamp = Column(DateTime, default=datetime.datetime.utcnow)
	# the client user that initiated this scan
	initiated_by = Column(Integer, ForeignKey("instagram_user.instagram_user_id"))

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

# an instagram media entity (photo, video, etc)
class Media(Base):
	__tablename__ = 'media'

	media_id = Column(BigInteger, primary_key=True)
	instagram_user_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)
	is_picture = Column(Boolean)

# a users comment
class Comment(Base):
	__tablename__ = 'comment'

	comment_id = Column(BigInteger, primary_key=True)
	media_id = Column(BigInteger, ForeignKey("media.media_id"), nullable=False)
	instagram_user_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)
	text = Column(String(length=4096), nullable=False)

# a non automated user engagement
class Interaction(Base):
	__tablename__ = 'interaction'

	interaction_id = Column(Integer, primary_key=True, autoincrement=True)
	# the account interacted with
	interacted_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)
	# the account that created the interaction
	interactor_id = Column(BigInteger, ForeignKey("instagram_user.instagram_user_id"), nullable=False)
