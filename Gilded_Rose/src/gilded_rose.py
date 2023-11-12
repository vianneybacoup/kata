# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if self.is_regular_item(item):
                self.try_decreasing_quality(item)
            elif item.name == "Aged Brie":
                self.try_increasing_quality(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self.try_increasing_quality(item)
                if item.sell_in < 11:
                    self.try_increasing_quality(item)

                if item.sell_in < 6:
                    self.try_increasing_quality(item)

            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1

            if item.sell_in < 0:
                if self.is_regular_item(item):
                    self.try_decreasing_quality(item)
                elif item.name == "Aged Brie":
                    self.try_increasing_quality(item)
                elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                    item.quality = 0

    def try_decreasing_quality(self, item):
        if self.has_quality(item):
            item.quality = item.quality - 1

    def has_quality(self, item):
        return item.quality > 0

    def try_increasing_quality(self, item):
        if self.is_quality_not_too_high(item):
            item.quality = item.quality + 1

    def is_quality_not_too_high(self, item):
        return item.quality < 50

    def is_regular_item(self, item):
        return item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert" and item.name != "Sulfuras, Hand of Ragnaros"


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)