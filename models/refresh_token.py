from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)

    token = Column(String, unique=True, index=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    expires_at = Column(DateTime, nullable=False)

    revoked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
