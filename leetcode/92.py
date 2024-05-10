# 92. Reverse Linked List II
# Given the head of a singly linked list and two integers left and right where 
# left <= right, reverse the nodes of the list from position left to position 
# right, and return the reversed list.

class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# soln 1 (top 6%)
def reverseBetween(self, head, left, right):
    """
    :type head: ListNode
    :type left: int
    :type right: int
    :rtype: ListNode
    """
    bef = back = head
    for i in range(left - 1):
        bef = back
        back = back.next
    
    mid = back
    for i in range(right - left):
        front = back.next
        back.next = front.next
        front.next = mid
        mid = front
    if left <= 1:
        return mid
    bef.next = mid
    return head

# soln 2
def reverseBetween(self, head, left, right):
    """
    :type head: ListNode
    :type left: int
    :type right: int
    :rtype: ListNode
    """
    preHead = ListNode(0, head)
    bef = preHead
    for i in range(left - 1):
        bef = bef.next
    mid = back = bef.next
    
    for i in range(right - left):
        front = back.next
        back.next = front.next
        front.next = mid
        mid = front
    
    bef.next = mid
    return preHead.next