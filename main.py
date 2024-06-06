from bs4 import BeautifulSoup
import requests
import csv


def get_book_data(category):
    """Fetches book data from Project Gutenberg"""
    category_formatted = category.replace(' ', '+')
    url = f'https://www.gutenberg.org/ebooks/search/?query={
        category_formatted}&submit_search=Go%21'
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    soup = BeautifulSoup(response.content, 'lxml')
    books = soup.find_all('li', class_='booklink')

    for book in books:
        title = book.find('span', class_='title').text.strip()
        author_tag = book.find('span', class_='subtitle')
        author = 'Author Unavailable' if author_tag is None else author_tag.text.strip()
        link = book.a['href']
        # Use a generator
        yield title, author, f'https://www.gutenberg.org{link}'


def main():
    print("Enter book category.")
    category = input('> ')

    print('Do you want to export the result to csv? "Y" or "N" ')
    export_to_csv = input('> ').upper() == 'Y'

    if export_to_csv:
        filename = f'{category}_books.csv'
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:  # 'w' mode for new file
            fieldnames = ['Title', 'Author', 'Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for title, author, link in get_book_data(category):
                writer.writerow(
                    {'Title': title, 'Author': author, 'Link': link})
        print(f'Exported as {filename}')
    else:
        for title, author, link in get_book_data(category):
            print(title)
            print(author)
            print(link)
            print('*****************************************************')


if __name__ == '__main__':
    main()
