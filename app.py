from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from funcs import convert_to_json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Book {self.name}>'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'<Customer {self.name}>'

def test():
    with app.app_context():
        print("Creating tables and adding data...")
        db.create_all()

        if not Book.query.first():
            new_books = [
                Book(name='lion in the desert', author='tesla', year=2000, active=True),
                Book(name='gal russo', author='me and you', year=2020, active=True),
                Book(name='erez habani', author='you and me', year=2022, active=True)
            ]
            db.session.add_all(new_books)
            db.session.commit()

        if not Customer.query.first():
            new_customers = [
                Customer(name='rotem', city='holon', age=20),
                Customer(name='eyal', city='ranana', age=30),
                Customer(name='nevo', city='petah-tikva', age=25)
            ]
            db.session.add_all(new_customers)
            db.session.commit()

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def def_book():
    if request.method == 'GET':
        books = Book.query.all()
        books_data = convert_to_json(books) 
        return books_data, 200
    elif request.method == 'POST':
        data = request.get_json()
        new_book = Book(
            name=data['name'],
            author=data['author'],
            year=data['year'],
            active=data.get('active', True)
        )
        db.session.add(new_book)
        db.session.commit()
        return {"message": "Book added successfully!"}, 201
    elif request.method == 'PUT':
        data = request.get_json()
        book = Book.query.get(data['id'])  
        if book:
            book.name = data['name']
            book.author = data['author']
            book.year = data['year']
            book.active = data['active']
            db.session.commit()
            return {"message": "Book updated successfully!"}
        else:
            return {"message": "Book not found!"}, 404
    elif request.method == 'DELETE':
        data = request.get_json()
        book = Book.query.get(data['id']) 
        if book:
            book.active = data['active']
            db.session.commit()
            return {"message": "Book status changed successfully!"}
        else:
            return {"message": "Book not found!"}, 404

if __name__ == "__main__":
    print("Starting the app...")  
    test() 
    print("Test function finished.") 
    app.run(debug=True)
