from src.db.database import Base, engine
from src.models.campground_orm import CampgroundORM

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")
