from bs4 import BeautifulSoup
import urllib.request
import datetime
import sys


def dump_to_file(url, content, file):
    f = open(file, 'a')
    f.write('{}:::{}:::{}\n'.format(url,content[0],content[1]))
    f.close

def read_cache(file):
    f = open(file,'r')
    url_title_dict = {}
    url_links_dict = {}
    for line in f.readlines():
        key = line.split(':::')[0]
        title_value = line.split(':::')[1]
        links_string = line.split(':::')[2]
        links_value = links_string[2:(len(links_string)-3)].split('\', \'')
        url_title_dict[key] = title_value
        url_links_dict[key] = links_value
    return url_title_dict, url_links_dict

def get_title_and_links(url):
    url_title_dict, url_links_dict = read_cache('wikipedia_storage.txt')
    if url in url_title_dict:
        title = url_title_dict[url]
        list_of_links = url_links_dict[url]
    else:
        try:
            page = urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            print('Cannot find ' + url + ' in Wikipedia!')
            return
        
        soup = BeautifulSoup(page.read(), 'html.parser')
        title = soup.find('h1').get_text()
        list_of_links = []
        body_content = soup.find(attrs={'class': 'mw-parser-output'})
        for link in body_content.find_all('a'):
            potential_link = link.get('href')
            if link.get('title') != None and '/wiki/' in potential_link and 'http' not in potential_link and ':' not in potential_link:
                link_url = str('https://en.wikipedia.org' + potential_link)
                if link_url not in list_of_links:
                    list_of_links.append(link_url)
        
        dump_to_file(url,[title,list_of_links],'wikipedia_storage.txt')

    return title, list_of_links


def main(start, destination):
    start_time = datetime.datetime.now()

    start_url = str('https://en.wikipedia.org/wiki/' + start)
    destination_url = str('https://en.wikipedia.org/wiki/' + destination)
    
    title, unvisited_links = get_title_and_links(start_url)
    if unvisited_links == None:
        return

    visited_links = [start_url]
    title_dict = {start_url:start, destination_url:destination}
    link_dict = {}
    for link in unvisited_links:
        link_dict[link] = start_url

    
    while len(unvisited_links) > 0:
        if destination_url in unvisited_links:
            break
        first_link = unvisited_links[0]
        #print(first_link)
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