from flask import Flask, request
import sqlite3
from funcs import convert_to_json

app = Flask(__name__)

conn = sqlite3.connect('books.db',check_same_thread=False)
cur = conn.cursor()


def test():
    # 3. Create a table (if it doesn't exist)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            active boolean DEFAULT True
        )
    ''')
    cur.execute("INSERT INTO books (name, author,year,active) VALUES ('lion in the desert', 'tesla',2000,1)")
    cur.execute("INSERT INTO books (name, author,year,active) VALUES ('gal russo', 'me and you',2020,1)")
    cur.execute("INSERT INTO books (name, author,year,active) VALUES ('erez habani', 'you and me',2022,1)")
    conn.commit()





@app.route('/', methods=['GET','DELETE','PUT','POST'])
def def_book():
    if request.method == 'GET':
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        json_data = convert_to_json(rows)  
        return json_data, 200 
    elif request.method == 'POST':
        data = request.get_json()
        cur.execute("INSERT INTO books (name, author, year, active) VALUES (?, ?, ?, ?)",
                    (data['name'], data['author'], data['year'], data.get('active', 1)))
        conn.commit()
        return {"message": "Book added successfully!"}, 201
    elif request.method == 'PUT':
        data = request.get_json()
        cur.execute("UPDATE books SET name = ?, author = ?, year = ?, active = ? WHERE id = ?",
                    (data['name'], data['author'], data['year'], data['active'], data['id']))
        conn.commit()
        return {"message": "Book updated successfully!"}
    elif request.method == 'DELETE':
        data = request.get_json()
        cur.execute("UPDATE books SET active = ? WHERE id = ?",
                    (data['active'], data['id']))
        conn.commit()
        return {"message": "Book status changed successfully!"}


if __name__ == "__main__":
    test()
    app.run(debug=True)