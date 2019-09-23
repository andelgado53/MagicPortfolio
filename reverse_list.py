class LinkedListNode(object):
    def __init__(self, value):
        self.value = value
        self.next  = None


a = LinkedListNode('a')
b = LinkedListNode('b')
c = LinkedListNode('c')
d = LinkedListNode('d')
e = LinkedListNode('e')

head = a
a.next = b
b.next = c 
c.next = d
d.next = e
x = head
while x:
    print(x.value)
    x = x.next

print("************************")

def reverse_list(node):
    stack = []
    stack.append(node.value)
    n = node.next
    while n:
        stack.append(n.value)
        n = n.next
    
    while len(stack) > 0:
        s = stack.pop()
        node.value = s
        if node.next:
            node = node.next
        else:
            node.next = None

    
# reverse_list(a)
# c = head
# while c:
#     print(c.value)
#     c = c.next

def reverse_list_in_place(node):
    previous = None
    current = node
    while current != None:
        temp = current.next
        current.next = previous
        previous = current
        current = temp
    return previous

c = reverse_list_in_place(head)
while c:
    print(c.value)
    c = c.next

