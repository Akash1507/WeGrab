from urllib.request import urlopen
from link_seeker import LinkFinder
from urls import *
from common import *


class Grabber:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Grabber.project_name = project_name
        Grabber.base_url = base_url
        Grabber.domain_name = domain_name
        Grabber.queue_file = Grabber.project_name + '/queue.txt'
        Grabber.crawled_file = Grabber.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Grabber.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Grabber.project_name)
        create_data_files(Grabber.project_name, Grabber.base_url)
        Grabber.queue = file_to_set(Grabber.queue_file)
        Grabber.crawled = file_to_set(Grabber.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Grabber.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Grabber.queue)) + ' | Crawled  ' + str(len(Grabber.crawled)))
            Grabber.add_links_to_queue(Grabber.gather_links(page_url))
            Grabber.queue.remove(page_url)
            Grabber.crawled.add(page_url)
            Grabber.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Grabber.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Grabber.queue) or (url in Grabber.crawled):
                continue
            if Grabber.domain_name != get_domain_name(url):
                continue
            Grabber.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Grabber.queue, Grabber.queue_file)
        set_to_file(Grabber.crawled, Grabber.crawled_file)
