from bs4 import BeautifulSoup
import urllib.request
import datetime
import sys


def get_title_and_links(link):

    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page.read(), 'html.parser')
    if soup == None:
        return

    title = soup.find('h1').get_text()

    body_content = soup.find(attrs={'class': 'mw-parser-output'})
    list_of_links = []
    for link in body_content.find_all('a'):
        potential_link = link.get('href')
        if link.get('title') != None and '/wiki/' in potential_link and 'http' not in potential_link and ':' not in potential_link:
            url = str('https://en.wikipedia.org' + potential_link)
            if url not in list_of_links:
                list_of_links.append(url)

    return title, list_of_links


def main(start,destination):
    start_time = datetime.datetime.now()

    start_url = str('https://en.wikipedia.org/wiki/' + start)
    destination_url = str('https://en.wikipedia.org/wiki/' + destination)
    for url in [start_url, destination_url]:
        try:
            urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            print('Cannot find ' + url + ' in Wikipedia!')
            return
    
    title, unvisited_links = get_title_and_links(start_url)
    visited_links = [start_url]
    title_dict = {start_url:start, destination_url:destination}
    link_dict = {}
    for link in unvisited_links:
        link_dict[link] = start_url

    while len(unvisited_links) > 0:
        first_link = unvisited_links[0]
        print(first_link)
        del unvisited_links[0]
        if first_link not in visited_links:
            visited_links.append(first_link)
            title, list_of_links = get_title_and_links(first_link)
            title_dict[first_link] = title
            if destination_url in list_of_links:
                link_dict[destination_url] = first_link
                break
            else:
                for link in list_of_links:
                    if link not in visited_links and link not in unvisited_links:
                        link_dict[link] = first_link
                        unvisited_links.append(link)
    
    key = destination_url
    reverse_path = [key]
    path = []
    while key != start_url:
        reverse_path.append(link_dict[key])
        key = link_dict[key]
    for link in reversed(reverse_path):
        subject = title_dict[link]
        path.append(subject)

    print('Shortest path from ' + start + ' to ' + destination + ': ' + str(path))
    print('Length of path: ' + str(len(path)-1))
    
    end_time = datetime.datetime.now()
    print('Runtime: ' + str(end_time - start_time))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('[Usage] path_finder.py [Start] [Destination]')
        sys.exit(-1)
    
    main(sys.argv[1],sys.argv[2])