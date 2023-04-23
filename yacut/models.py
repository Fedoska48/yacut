from datetime import datetime

from settings import API_FIELDS, DOMAIN
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text(512), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Преобразование объекта модели в словарь (словарь -> JSON)."""
        return dict(
            url=self.original,
            short_link=DOMAIN + self.short,
        )

    def from_dict(self, data):
        """Преобразование словаря в объект модели (JSON -> словарь).
        В пустой объект класса URLMap добавляются поля полученные в POST."""
        for field in API_FIELDS:
            if field in data:
                setattr(self, API_FIELDS[field], data[field])
