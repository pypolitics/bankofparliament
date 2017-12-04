from constants import NAME_TITLES

node_id = 0
def make_node(node, name, hovertext, node_type, hyperlink=None, unique=True):
    """"""
    if unique:
        global node_id
        node_id += 1
        node['id'] = node_id

    node['name'] = name
    node['hovertext'] = hovertext
    node['node_type'] = node_type
    node['hyperlink'] = hyperlink
    node['border_style'] = {'color' : 'rgb(50,50,50)', 'size' : 0.5}
    return node

def make_link(link, nodes, source, target):
    """"""

    link['source'] = nodes.index(source)
    link['target'] = nodes.index(target)
    return link

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def clean_name(name):
    name_list = []

    for n in name.lower().split(' '):
        if n not in NAME_TITLES:
            name_list.append(n)

    return ' '.join(name_list).lower().strip()

def padded_string(string, padding=100):
    """
    Return a padded string
    """
    return string.ljust(padding)    