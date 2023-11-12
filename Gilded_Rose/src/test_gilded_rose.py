# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


GENERIC_ITEM = "Generic Item"
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"

TOO_LATE = -1
STILL_TIME = 1

CLOSE_ENOUGH = 4
GETTING_CLOSER = 8
FAR_ENOUGH = 12

NO_QUALITY = 0
TOO_SMALL_QUALITY = 1
GENERIC_QUALITY = 10
MAX_QUALITY = 50


def init_gilded_rose_and_update_quality(items):
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual("foo", items[0].name)

    def test_when_no_items_then_no_issues(self):
        items = []
        init_gilded_rose_and_update_quality(items)
        self.defaultTestResult()

    def test_when_quality_is_0_and_date_not_passed_then_quality_stays_0(self):
        items = [Item(GENERIC_ITEM, STILL_TIME, NO_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(NO_QUALITY, items[0].quality)

    def test_when_quality_is_0_and_date_passed_then_quality_stays_0(self):
        items = [Item(GENERIC_ITEM, TOO_LATE, NO_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(NO_QUALITY, items[0].quality)

    def test_when_quality_is_1_and_date_passed_then_quality_dont_drop_below_0(self):
        items = [Item(GENERIC_ITEM, TOO_LATE, TOO_SMALL_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(NO_QUALITY, items[0].quality)

    def test_when_quality_and_date_higher_than_0_then_both_should_decrease_by_1(self):
        items = [Item(GENERIC_ITEM, STILL_TIME, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(STILL_TIME - 1, items[0].sell_in)
        self.assertEqual(GENERIC_QUALITY - 1, items[0].quality)

    def test_when_sell_in_passed_then_quality_should_decrease_twice_as_fast(self):
        items = [Item(GENERIC_ITEM, TOO_LATE, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(GENERIC_QUALITY - 2, items[0].quality)

    def test_when_item_is_aged_brie_then_quality_increases(self):
        items = [Item(AGED_BRIE, STILL_TIME, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(GENERIC_QUALITY + 1, items[0].quality)

    def test_when_item_is_aged_brie_and_sell_in_passed_then_quality_increases_twice(self):
        items = [Item(AGED_BRIE, TOO_LATE, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(GENERIC_QUALITY + 2, items[0].quality)

    def test_when_increasing_quality_it_can_not_be_higher_than_50(self):
        items = [Item(AGED_BRIE, STILL_TIME, MAX_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(MAX_QUALITY, items[0].quality)

    def test_when_sulfuras_is_sold_sell_in_and_quality_never_decreases(self):
        items = [Item(SULFURAS, STILL_TIME, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(STILL_TIME, items[0].sell_in)
        self.assertEqual(GENERIC_QUALITY, items[0].quality)

    def test_when_backstage_passes_and_sell_in_more_than_10_increase_quality_once(self):
        items = [Item(BACKSTAGE_PASSES, FAR_ENOUGH, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(GENERIC_QUALITY + 1, items[0].quality)

    def test_when_backstage_passes_and_sell_in_less_than_10_increase_quality_twice(self):
        items = [Item(BACKSTAGE_PASSES, GETTING_CLOSER, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(GENERIC_QUALITY + 2, items[0].quality)

    def test_when_backstage_passes_and_sell_in_less_than_5_increase_quality_thrice(self):
        items = [Item(BACKSTAGE_PASSES, CLOSE_ENOUGH, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(GENERIC_QUALITY + 3, items[0].quality)

    def test_when_backstage_passes_and_sell_in_less_than_0_then_quality_should_be_0(self):
        items = [Item(BACKSTAGE_PASSES, TOO_LATE, GENERIC_QUALITY)]
        init_gilded_rose_and_update_quality(items)
        self.assertEqual(NO_QUALITY, items[0].quality)


if __name__ == '__main__':
    unittest.main()
