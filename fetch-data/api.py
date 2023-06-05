import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://gutendex.com/books?languages=en,fr'

def dl_books_from_page(url):
    ''' Download json of the page and return books and next token'''
    response = requests.get(url)
    if response.status_code == 200:
        books_data = response.json()
        next = books_data['next']
        books = books_data['results']
        return books, next
    else:
        return None, None

def parse_books_from_json(json):
    ''' Parse books from json to dict '''
    books = []
    for book in json:
        if 'text/plain' in book['formats'] and book['authors']:
            books.append({
                'id': book['id'],
                'title': book['title'],
                'authors': book['authors'][0]['name'],
                'subjects': book['subjects'],
                'languages': book['languages'],
                'formats': book['formats']['text/plain'],
                'download_count': book['download_count']
            })
    return books

def save_book_from_url(url):
    ''' Save book from formats-URL to raw_data folder'''
    response = requests.get(url)
    if response.status_code == 200:
        file_name_with_extension = os.path.basename(url)
        file_name, extension = os.path.splitext(file_name_with_extension)
        file_path = 'raw_data/books/' + file_name
        with open(file_path, 'w') as file:
            file.write(response.text.encode('utf-8').decode('utf-8'))

def download_all_books():
    ''' Download all books from the website, save them as .txt files and return a dataframe with the books metadata'''
    next_page = url
    while next_page:
        books, next_page = dl_books_from_page(next_page)
        if books:
            parsed_books = parse_books_from_json(books)
            for book in parsed_books:
                download_url = book['formats']
                save_book_from_url(download_url)
                print(book['title'], '... downloaded')

                # save each book as a row in a csv file
                with open('raw_data/csv/books.csv', 'a') as file:
                    subjects_str = ', '.join(book['subjects']).replace('"', '').replace(',', '')
                    title = book['title'].replace('"', '').replace(',', '')
                    authors = book['authors'].replace('"', '').replace(',', '')
                    languages = book['languages'][0]
                    formats = book['formats'].replace('"', '').replace(',', '')

                    file.write(f"{book['id']},{title},{authors},{subjects_str},{languages},{formats},{book['download_count']}\n")

download_all_books()


# print(dl_books_from_page(url))
# print("*******************")
# print(parse_books_from_json(dl_books_from_page(url)[0]))
# print("*******************")
# print(save_book_from_url('https://www.gutenberg.org/ebooks/64317.txt.utf-8'))
