# -*- coding: utf-8 -*-
'''DelogX.utils.compat

Utils about compatibility of OS and Python.
'''


class Compat(object):
    '''Compatibility utils.'''

    @classmethod
    def cmp_to_key(cls):
        '''Return a class which convert cmp function to key function.

        Returns:

            class: Class to convert cmp function to key function.
        '''
        return CmpToKey


class CmpToKey(object):
    '''Convert cmp function to key function in `sorted()`.'''

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return self.sort_compare(self.obj, other.obj) < 0

    def __gt__(self, other):
        return self.sort_compare(self.obj, other.obj) > 0

    def __eq__(self, other):
        return self.sort_compare(self.obj, other.obj) == 0

    def __le__(self, other):
        return self.sort_compare(self.obj, other.obj) <= 0

    def __ge__(self, other):
        return self.sort_compare(self.obj, other.obj) >= 0

    def __ne__(self, other):
        return self.sort_compare(self.obj, other.obj) != 0

    @classmethod
    def sort_compare(cls, item_a, item_b):
        '''The cmp function to compare `DelogX.entity.item.Page`.

        Args:

            item_a (object): First object to compare.
            item_b (object): Second object.

        Returns:

            int: 0 is `a = b`, positive is `a > b`, negative is `a < b`.
        '''
        a_sort = item_a[1].sort
        b_sort = item_b[1].sort
        if a_sort is not None and b_sort is not None:
            return a_sort - b_sort
        elif a_sort is None and b_sort is None:
            return 0
        elif a_sort is None:
            return 1
        else:
            return -1
