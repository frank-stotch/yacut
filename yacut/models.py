from datetime import datetime, timezone

from yacut import db


class MaxLength:
    ORIGINAL_URL = 256
    SHORT_URL = 256


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MaxLength.ORIGINAL_URL), nullable=False)
    short = db.Column(db.String(MaxLength.ORIGINAL_URL), nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.now(timezone.utc))

    @classmethod
    def get_user_defined_fields_names(cls):
        return [
            column.name for column in cls.__table__.columns
            if not column.primary_key
            and not column.default
            and not column.server_default
            and not column.nullable
        ]

    @classmethod
    def get_all_fields_names(cls):
        return [column.name for column in cls.__table__.columns]

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            field_name: getattr(self, field_name)
            for field_name in self.get_all_fields_names()
        }

    def from_dict(self, data: dict):
        for field in self.get_user_defined_fields_names():
            if field in data:
                setattr(self, field, data[field])