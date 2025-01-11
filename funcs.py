import json


def convert_to_json(rows):
    # Convert a list of tuples to a list of dictionaries
    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "name": row[1],
            "author": row[2],
            "year": row[3],
            "active": bool(row[4])
        })
    return json.dumps(books)  # Convert the list of dictionaries to JSON string



