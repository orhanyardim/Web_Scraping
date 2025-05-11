from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base

class CampgroundORM(Base):
    __tablename__ = "campgrounds"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    region_name: Mapped[str] = mapped_column(String, nullable=False)

    administrative_area: Mapped[str] = mapped_column(String, nullable=True)
    nearest_city_name: Mapped[str] = mapped_column(String, nullable=True)
    accommodation_type_names: Mapped[list[str]] = mapped_column(PG_ARRAY(String))
    bookable: Mapped[bool] = mapped_column(Boolean, default=False)
    camper_types: Mapped[list[str]] = mapped_column(PG_ARRAY(String))
    operator: Mapped[str] = mapped_column(String, nullable=True)

    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    photo_urls: Mapped[list[str]] = mapped_column(PG_ARRAY(String))
    photos_count: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    reviews_count: Mapped[int] = mapped_column(Integer, default=0)
    slug: Mapped[str] = mapped_column(String, nullable=True)
    price_low: Mapped[float] = mapped_column(Float, nullable=True)
    price_high: Mapped[float] = mapped_column(Float, nullable=True)
    availability_updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    detail_url: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)  # <-- Yeni eklenen alan
