from random import choice as rc
from random import randint

from app import app
from faker import Faker
from models import Cheese, Producer, db

fake = Faker()


def clear_tables():
    print("Clearing database...")
    Producer.query.delete()
    Cheese.query.delete()


def seed_producers():
    print("Adding producers...")

    for _ in range(10):
        producer = Producer(name=fake.company())
        db.session.add(producer)
        db.session.commit()


def seed_cheeses():
    print("Adding cheeses...")
    for _ in range(100):
        cheese = Cheese(
            name=fake.word(),
            price=randint(1, 100),
            producer_id=rc(Producer.query.all()).id,
        )
        db.session.add(cheese)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        clear_tables()
        seed_producers()
        seed_cheeses()
        print("Done!")
