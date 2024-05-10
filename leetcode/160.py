# Given the heads of two singly linked-lists headA and headB, return the node 
# at which the two lists intersect. If the two linked lists have no 
# intersection at all, return null.

class Solution(object):
    def getIntersectionNode(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """
        a = headA
        b = headB
        endA = endB = False
        while a != b:
            if a.next:
                a = a.next
            elif endA:
                return None
            else:
                a = headB
                endA = True
            if b.next:
                b = b.next
            elif endB:
                return None
            else:
                b = headA
                endB = True
        return a