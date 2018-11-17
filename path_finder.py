from bs4 import BeautifulSoup
import urllib.request
import datetime
import sys


def get_links(link):

    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page.read(), 'html.parser').find(attrs={'class': 'mw-parser-output'})
    print(sys.getsizeof(soup))
    if soup == None:
        return

    list_of_links = []
    for link in soup.find_all('a'):
        potential_link = link.get('href')
        if link.get('title') != None and '/wiki/' in potential_link and 'http' not in potential_link and ':' not in potential_link:
            url = str('https://en.wikipedia.org' + potential_link)
            if url not in list_of_links:
                list_of_links.append(url)

    return list_of_links


def find_subject(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), 'html.parser').find(attrs={'id': 'firstHeading'})
    return soup.get_text()


def main(start,destination):
    
    start_url = str('https://en.wikipedia.org/wiki/' + start)
    try:
        urllib.request.urlopen(start_url)
    except urllib.error.HTTPError:
        print('Cannot find ' + start + ' in Wikipedia!')
        return
    destination_url = str('https://en.wikipedia.org/wiki/' + destination)
    try:
        urllib.request.urlopen(destination_url)
    except urllib.error.HTTPError:
        print('Cannot find ' + destination + ' in Wikipedia!')
        return
    
    list_of_links = get_links(start_url)
    all_visited_links = []
    link_dict = {}

    while len(list_of_links) > 0:
        first_link = list_of_links[0]
        del list_of_links[0]
        print(first_link)
        if first_link not in all_visited_links:
            all_visited_links.append(first_link)
            links = get_links(first_link)
            if destination_url in links:
                link_dict[destination_url] = first_link
                break
            else:
                for link in links:
                    if link not in all_visited_links:
                        link_dict[link] = first_link
                    if link not in list_of_links:
                        list_of_links.append(link)
    
    key = destination_url
    reverse_path = [key]
    while len(link_dict) > 0:
        if key in link_dict:
            reverse_path.append(link_dict[key])
            key = link_dict[key]
        else:
            break 

    path = []
    for link in reversed(reverse_path):
        subject = find_subject(link)
        path.append(subject)
        
    path_length = len(reverse_path)

    print(path)
    print(path_length)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('[Usage] path_finder.py [start-page] [end-page]')
        sys.exit(-1)
    
    main(sys.argv[1],sys.argv[2])