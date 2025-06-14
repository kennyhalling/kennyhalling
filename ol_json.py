import requests
import json
import random

headers = {"User-Agent": "Mozilla/5.0"}
serial_counter = 1

def search_books(subject, serial_counter, limit=200,):
    url = f"https://openlibrary.org/search.json?subject={subject}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        books = data.get("docs", [])[:limit]
        
        simplified_books = []
        
        for book in books:
            title = book.get("title", "N/A")
            author = ", ".join(book.get("author_name", ["N/A"]))
            language = ", ".join(book.get("language", ["N/A"]))
            
            # Create 1 to 3 copies
            num_copies = random.randint(1, 3)
            for _ in range(num_copies):
                simplified_books.append({
                    "serial": f"{serial_counter:03d}",
                    "title": title,
                    "author": author,
                    "languages": language,
                    "available": True
                })
                serial_counter += 1
                
        return simplified_books
    else:
        print(f"Error fetching {subject}: {response.status_code}")
        return []

# Get fiction and non-fiction books
fiction_books = search_books("fiction", serial_counter, limit=200)
nonfiction_books = search_books("non-fiction", serial_counter+300, limit=200)

# Combine and save
combined = fiction_books + nonfiction_books

with open("book_inventory.json", "w", encoding="utf-8") as file:
    json.dump(combined, file, indent=4, ensure_ascii=False)

print("Book inventory saved to book_inventory.json")
