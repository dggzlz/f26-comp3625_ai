"""
This file contains useful objects for representing wikipedia pages and their links

DON'T EDIT THIS FILE. Do your work in main.py
"""


import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import List


class Node(ABC):
    """ abstract class representing a node in a search problem"""

    def __init__(self, state, parent=None, action=None, path_cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self._children = None

    @property
    def children(self):
        if self._children is None:
            self._children = self._get_children()
        return self._children

    @abstractmethod
    def _get_children(self):
        raise NotImplementedError()

    def get_ancestors(self):
        ancestors = [self]
        if self.parent:
            ancestors = self.parent.get_ancestors() + ancestors
        return ancestors

    def __repr__(self):
        num_children = f'{len(self._children)} children' if self._children else "not expanded"
        return f"{self.state} ({num_children})"

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return self.state.__hash__()


class WikiPage(Node):

    def __init__(self, url: str, parent: Node = None, path_cost: float = 0):
        super().__init__(
            state=url.replace('https://en.wikipedia.org/wiki/', '').replace('/wiki/', ''),
            parent=parent,
            path_cost=path_cost,
        )
        self.page_text = None

    def _get_children(self) -> List[Node]:
        print('getting html for', 'https://en.wikipedia.org/wiki/' + self.state)

        headers = {
            'User-Agent': 'Mount Royal University course about search algorithms (echalmers@mtroyal.ca)'
        }
        r = requests.get('https://en.wikipedia.org/wiki/' + self.state, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        body = soup.find("div", {"id": "bodyContent"})

        links = {x.get('href') for x in body.find_all('a')}
        links.discard(None)
        links = [x for x in links if x.startswith('/wiki') and ('Help:' not in x) and ('Special:' not in x) and ('File:' not in x)]

        return [WikiPage(link, parent=self, path_cost=self.path_cost + 1) for link in links]

    def get_page_text(self) -> str:
        if self.page_text is None:
            print('getting html for', 'https://en.wikipedia.org/wiki/' + self.state)
            r = requests.get('https://en.wikipedia.org/wiki/' + self.state)
            soup = BeautifulSoup(r.text, 'html.parser')
            body = soup.find("div", {"id": "bodyContent"})
            self.page_text = body.get_text(' ', strip=True)
        return self.page_text


if __name__ == '__main__':

    # instantiate an object representing a particular wiki page:
    page = WikiPage('https://en.wikipedia.org/wiki/Mount_Royal_University')

    # by default, the object is not expanded, meaning we don't know what its children are
    print(page)  # prints "Mount_Royal_University (not expanded)"

    # accessing the children attribute expands the page
    children = page.children  # returns a list of new WikiPage objects, accessible from page
    print(page)  # now prints "Mount_Royal_University (N children)"
    child_0 = page.children[0]

    # calling get_ancestors() returns a list of pages along the path to the page
    print(child_0.get_ancestors())  # prints a list with 2 pages, the first of which is the MRU page

    # two page objects can be checked for equality
    destination = WikiPage("https://en.wikipedia.org/wiki/Artificial_intelligence")
    page == destination  # False