from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class ParcelReservation(Base):
    __tablename__ = 'parcel_reservations'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parcel_id = Column(String, ForeignKey('parcels.id'), nullable=False)
    reserved_by = Column(String, ForeignKey('users.id'), nullable=False)
    reservation_date = Column(DateTime, default=datetime.now, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default='active')
    purpose = Column(Text)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    parcel = relationship("Parcel", backref="reservations")
    reserver = relationship("User", backref="reservations")

class VerificationLog(Base):
    __tablename__ = 'verification_logs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parcel_id = Column(String, ForeignKey('parcels.id'), nullable=False)
    checked_by = Column(String, ForeignKey('users.id'), nullable=False)
    check_timestamp = Column(DateTime, default=datetime.now, nullable=False)
    result = Column(String, nullable=False) # 'available' or 'unavailable'
    reason = Column(String)
    conflict_details = Column(Text)

    parcel = relationship("Parcel", backref="verification_logs")
    checker = relationship("User", backref="verification_logs")
    
    def to_dict(self):
        return {
            'id': self.id,
            'parcel_id': self.parcel_id,
            'checked_by': self.checked_by,
            'check_timestamp': self.check_timestamp.isoformat() if self.check_timestamp else None,
            'result': self.result,
            'reason': self.reason,
            'conflict_details': self.conflict_details
        }
