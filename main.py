from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os
import time
def generate_links(names):
    #print('generating links')
    new_names = []
    for name in names:
        new_names.append('http://flibusta.net/g/%s/Pop' % (name))
    #print('finish generating links')
    return new_names


def download_epubs(links, limit):
    #print('begin download epubs')
    for link in links:
     #   print('for link in links')
        gurl = urlopen(link)
        gsoup = BeautifulSoup(gurl)
        title = gsoup.html.head.title.string.split(' | ')[0]
        if not os.path.exists(title):
            os.makedirs(title)
        book_links = gsoup.find_all('a', attrs={'href': re.compile('^/b/.*')})
        loadlinks = []
        #print('book_link in book_links')
        for book_link in book_links:
            loadlinks.append((book_link.string, 'http://flibusta.net%s/epub' % book_link['href']))
        i = 1
        for loadlink in loadlinks:
           # print('begin loading the book')
            now = time.clock()
            if i == limit:
                break
            book_url = urlopen(loadlink[1])
            book = book_url.read()
            try:
                book.decode('utf-8')
                print('Book %s is blocked'%loadlink[0])
                continue
            except UnicodeDecodeError:
                pass

            book_name = '%s/%s.epub' % (title, loadlink[0])
            f = open(book_name, 'wb')
            f.write(book)
            f.close()
            print('%d/%d (%s) [%f]' % (i, len(loadlinks), book_name, (time.clock() - now) * 100))
            i += 1
#            print('finish loading the book')
        else:
            print('Finished %s'%title)



if __name__ == '__main__':
    url = urlopen('http://flibusta.net/g')
    soup = BeautifulSoup(url)
    links = soup.find_all('a', attrs={'name': re.compile('^.*')})
    names = ['det_political', 'det_police', 'det_maniac', 'det_su', 'thriller',
             'det_espionage', 'military_special', 'adv_indian', 'adv_history', 'adv_maritime', 'adventure',
             'adv_modern']
    #'det_action', 'detective', 'det_irony','det_history', 'det_classic', 'det_crime', 'det_hard',
    # for link in links:
    #    names.append(link['name'])

    links = generate_links(names)
    download_epubs(links, 200)
