import pandas as pd
import os

def get_books_from_famous_authors():
    '''Return a list of all files from raw_data/books_most_famous'''
    return os.listdir('fetch-data/raw_data/books_most_famous')

def get_author_name(filename):
    '''Get author name from filename'''
    filename = filename.split('.')[0]    # remove extension
    with open('fetch-data/raw_data/csv/books.csv', 'r') as file:
        for line in file:
            if filename in line:
                return line.split(',')[2] # return author name

def read_book(book_id):
    '''Read book from file'''
    file_name = 'fetch-data/raw_data/books_most_famous/' + book_id
    with open(file_name, 'r') as file:
        return file.read()

def chunk_text(text, chunk_size=256):
    '''Chunking data into chunks of size chunk_size'''
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    print(str(len(chunks)) + ' chunks created')
    return chunks

def save_all_books_to_dataframe():
    data = []
    book_files = get_books_from_famous_authors()
    for file in book_files:
        author_name = get_author_name(file)
        book_text = read_book(file)
        chunks = chunk_text(book_text)
        for i, chunk in enumerate(chunks):
            data.append({"Author": author_name, "Chunk": chunk})
    df = pd.DataFrame(data)
    return df

# print(save_all_books_to_dataframe())
print(get_books_from_famous_authors())
