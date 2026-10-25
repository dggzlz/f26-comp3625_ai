from nodes import WikiPage

# instantiate an object representing a particular wiki page:
page = WikiPage('https://en.wikipedia.org/wiki/Mount_Royal_University')


# by default, the object is not expanded, meaning we don't know what its children are
print(page)    # prints "Mount_Royal_University (not expanded)"


# accessing the children attribute expands the page
children = page.children  # returns a list of new WikiPage objects, accessible from page
print(page)  # now prints "Mount_Royal_University (N children)"

# calling get_ancestors() returns a list of pages along the path to the page
child_0 = children[0]
print(child_0.get_ancestors())  # prints a list of pages along the route

# two page objects can be checked for equality
destination = WikiPage("https://en.wikipedia.org/wiki/Artificial_intelligence")
page == destination  # False

