# -*- coding: utf-8 -*-
from item_constants import *


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if GildedRose.is_regular_item(item):
                GildedRose.try_decreasing_quality(item)
            elif item.name == AGED_BRIE:
                GildedRose.try_increasing_quality(item)
            elif item.name == BACKSTAGE:
                GildedRose.try_increasing_quality(item)
                if item.sell_in < 11:
                    GildedRose.try_increasing_quality(item)

                if item.sell_in < 6:
                    GildedRose.try_increasing_quality(item)

            if item.name != SULFURAS:
                item.sell_in = item.sell_in - 1

            if GildedRose.is_selling_date_passed(item):
                if GildedRose.is_regular_item(item):
                    GildedRose.try_decreasing_quality(item)
                elif item.name == AGED_BRIE:
                    GildedRose.try_increasing_quality(item)
                elif item.name == BACKSTAGE:
                    item.quality = 0

    @staticmethod
    def is_selling_date_passed(item):
        return item.sell_in < 0

    @staticmethod
    def try_decreasing_quality(item):
        if GildedRose.has_quality(item):
            item.quality = item.quality - 1

    @staticmethod
    def has_quality(item):
        return item.quality > 0

    @staticmethod
    def try_increasing_quality(item):
        if GildedRose.is_quality_not_too_high(item):
            item.quality = item.quality + 1

    @staticmethod
    def is_quality_not_too_high(item):
        return item.quality < 50

    @staticmethod
    def is_regular_item(item):
        return item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert" and item.name != "Sulfuras, Hand of Ragnaros"


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
