#!/usr/bin/python
class FilterModule(object):
    def filters(self):
        return {
            'amend_list_items': self.amend_list_items
        }

    def amend_list_items(self, orig_list, prefix="", postfix=""):
        return list(map(lambda listelement: prefix +
                        str(listelement) + postfix, orig_list))
