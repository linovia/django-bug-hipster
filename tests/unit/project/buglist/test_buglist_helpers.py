"""
bughipster.website.views
~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from bughipster.website.views import item_per_project, remove_duplicates



class Item(object):
    def __init__(self, id, product_id, value=''):
        self.id = id
        self.product_id = product_id
        self.value = value


def test_item_per_project():
    data = [Item(1, 1), Item(2, 1), Item(3, 1), Item(4, 2)]
    result = item_per_project(data)
    assert result == {1: [1, 2, 3], 2: [4]}


def test_remove_duplicates():
    data = [
        Item(1, 1, 'alpha'), Item(2, 2, 'alpha'),
        Item(3, 3, 'alpha'), Item(4, 1, 'beta')
    ]
    result = remove_duplicates(data)
    assert len(result) == 2
    assert result[0] == {2: 3, 1: 3}
    assert result[1] == {3: 2}
