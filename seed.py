from models import User, db, connect_db
from app import app

app = app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

# Add Users
kyle = User(first_name="Kyle", last_name="Akers", image="https://st2.depositphotos.com/4568293/7690/i/950/depositphotos_76902469-stock-photo-young-winner-happy-man-on.jpg")
andrew = User(first_name="Andrew", last_name="Donaldson", image="https://st2.depositphotos.com/4568293/7690/i/950/depositphotos_76902469-stock-photo-young-winner-happy-man-on.jpg")
goku = User(first_name="Goku", last_name="Saiyan", image="https://st2.depositphotos.com/4568293/7690/i/950/depositphotos_76902469-stock-photo-young-winner-happy-man-on.jpg")


# Add new objects to session, so they'll persist
with app.app_context():
    db.session.add(kyle)
    db.session.add(andrew)
    db.session.add(goku)

# Commit--otherwise, this never gets saved!
    db.session.commit()

