# Efficient subtree indexing (proof-of-concept)

class Tree:
    
    base_id = 0
    
    def __init__(self, name, children=None):
        Tree.base_id += 1
        self.id = Tree.base_id  # assign a unique id.
        self.name = name
        self.children = children or []
        return

    def dump(self, edge='', indent=0):
        print ('%s%s:%s(%d)' % (indent*'  ', edge, self.name, self.id))
        for (e,c) in self.children:
            c.dump(e, indent+1)
        return

node_id = {}
def get_node_id(parent, label):
    k = (parent, label)
    if k in node_id:
        nid = node_id[k]
    else:
        nid = node_id[k] = len(node_id)+1
    return nid

node_value = {}
def add_node_value(nid, value):
    if nid in node_value:
        a = node_value[nid]
    else:
        a = node_value[nid] = []
    a.append(value)
    return
        
def index_tree(tree):
    added = set()
    for (edge, child) in tree.children:
        for parent in index_tree(child):
            label = (edge+':'+tree.name)
            nid = get_node_id(parent, label)
            added.add(nid)
    label = (':'+tree.name)
    nid = get_node_id(None, label)
    added.add(nid)
    for nid in added:
        add_node_value(nid, tree.id)
    return added

def search_tree(labels):
    nid = None
    for label in labels:
        k = (nid, label)
        if k not in node_id: return None
        nid = node_id[k]
    return node_value[nid]

tree1 = Tree('A', [('b', Tree('B', [('c', Tree('C')),
                                    ('d', Tree('D'))])),
                   ('e', Tree('E'))])

tree2 = Tree('B', [('c', Tree('C')),
                   ('d', Tree('D'))])

tree3 = Tree('A', [('e', Tree('E', [('c', Tree('C'))]))])

tree1.dump()
tree2.dump()
tree3.dump()
index_tree(tree1)
index_tree(tree2)
index_tree(tree3)

#print (node_id)
#print (node_value)
print (search_tree([':C', 'c:B']))
print (search_tree([':D', 'd:B']))
print (search_tree([':B', 'b:A']))
print (search_tree([':E', 'e:A']))
