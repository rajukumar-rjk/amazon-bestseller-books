import requests
from bs4 import BeautifulSoup
from os import path
import csv
pageNo = 1
totalPage = 2
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
#            "Accept-Encoding": "gzip, deflate",
#            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
#            "Connection": "close", "Upgrade-Insecure-Requests": "1"}


def save_html(file_name, file_content):
    '''# this function is to save html only just to check html file better way. '''
    file =  open(file_name,'w')
    file.write(file_content.prettify())
    file.close()
    return ('file - ' + file_name + 'has been saved')


csv_file = open('amazon-bestsellers-books.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['book_rank',
                     'book_name', 'book_author',
                     'book_star', 'book_total_reviews',
                     'paper_type', 'price'])

while pageNo <= totalPage:
    if path.isfile('amazon-bestsellar-books-'+str(pageNo)+'.html'):
        with open('amazon-bestsellar-books-'+str(pageNo)+'.html') as source:
            soup = BeautifulSoup(source, 'html.parser')
            print('file has been loaded from local')
    else:
        source = requests.get(
            'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_' + str(pageNo) + '?ie=UTF8&pg=' + str(pageNo)
        )

        soup = BeautifulSoup(source.content, 'html.parser')

        html_file = open('amazon-bestsellar-books-'+str(pageNo)+'.html', 'w')
        html_file.write(soup.prettify())
        html_file.close()
        print('file has been saved on the local')

        print('scraping starts for page = ' + str(pageNo))

    # Now scrapping books for page 1
    for book_list in soup.find_all('li', class_='zg-item-immersion'):
        # save_html('book_list.html', book_list)

        # book rank and removing unwanted spaces
        try:
            book_rank = book_list.find('span', class_='zg-badge-text').text
            book_rank = " ".join(book_rank.split())
            print(book_rank)
        except Exception as e:
            book_rank = None

        # book name and removing unwanted spaces
        try:
            book_name = book_list.find('div', class_='p13n-sc-truncate p13n-sc-line-clamp-1 p13n-sc-truncate-desktop-type2').text
            book_name = " ".join(book_name.split())
            print(book_name)
        except Exception as e:
            book_name = None

        # book author and removing unwanted spaces (little different way this time, it works same as previous method)
        try:
            book_author = book_list.find('a', attrs={'class':'a-size-small a-link-child'}).text
            book_author = " ".join(book_author.split())
            print(book_author)
        except Exception as e:
            try:
                book_author = book_list.find('span', attrs={'class':'a-size-small a-color-base'}).text
                book_author = " ".join(book_author.split())
            except:
                book_author = None

        # total star and reviews
        try:
            book_stars = book_list.find('span', class_='a-icon-alt').text
            book_start = " ".join(book_stars.split())
            print(book_stars)
        except Exception as e:
            book_stars = 0

        try:
            book_reviews = book_list.find('a', attrs={'class':'a-size-small a-link-normal'}).text
            book_reviews = " ".join(book_reviews.split())
            print(book_reviews)
        except Exception as e:
            book_reviews = 0

        try:
            book_paper_type = book_list.find('span', attrs={'class': 'a-size-small a-color-secondary'}).text
            book_paper_type = " ".join(book_paper_type.split())
            print(book_paper_type)
        except Exception as e:
            book_paper_type = None
        try:
            book_price = book_list.find('span', attrs={'class': 'p13n-sc-price'}).text
            book_price = " ".join(book_price.split())
            print(book_price)
        except Exception as e:
            book_price = None

        csv_writer.writerow([book_rank,
                             book_name, book_author,
                             book_stars, book_reviews,
                             book_paper_type, book_price])

        print('scraping done for page = ' + str(pageNo))
    pageNo += 1

csv_file.close()