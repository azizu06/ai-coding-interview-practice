import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inventory import Inventory, Item  # noqa: E402


class TestAddItem(unittest.TestCase):
    def test_adds_valid_item(self):
        inventory = Inventory()
        self.assertTrue(inventory.add_item("anvil", 9))
        self.assertEqual(len(inventory), 1)
        self.assertIn("anvil", inventory)

    def test_rejects_negative_weight(self):
        inventory = Inventory()
        self.assertFalse(inventory.add_item("balloon", -1))
        self.assertEqual(len(inventory), 0)

    def test_rejects_non_integer_weight(self):
        inventory = Inventory()
        self.assertFalse(inventory.add_item("cloud", 2.5))
        self.assertFalse(inventory.add_item("cloud", "3"))

    def test_rejects_duplicate_name(self):
        inventory = Inventory([("anvil", 9)])
        self.assertFalse(inventory.add_item("anvil", 4))
        self.assertEqual(inventory.total_weight(), 9)

    # def test_rejects_zero_weight(self):
    #     inventory = Inventory()
    #     expected = "????"
    #     self.assertEqual(inventory.add_item("feather", 0), expected)
    #     self.assertEqual(len(inventory), 0)

    # def test_constructor_skips_invalid_pairs(self):
    #     inventory = Inventory([("anvil", 9), ("ghost", 0), ("hat", -2), ("anvil", 1)])
    #     expected_count = "????"
    #     self.assertEqual(len(inventory), expected_count)


class TestOrdering(unittest.TestCase):
    def test_total_weight(self):
        inventory = Inventory([("anvil", 9), ("book", 3), ("cup", 3)])
        self.assertEqual(inventory.total_weight(), 15)

    def test_items_keep_insertion_order(self):
        inventory = Inventory([("book", 3), ("anvil", 9)])
        self.assertEqual(inventory.items(), [Item("book", 3), Item("anvil", 9)])

    def test_heaviest_first(self):
        inventory = Inventory([("book", 3), ("anvil", 9), ("dish", 4)])
        self.assertEqual([item.name for item in inventory.items_by_weight()], ["anvil", "dish", "book"])

    def test_heaviest(self):
        inventory = Inventory([("book", 3), ("anvil", 9)])
        self.assertEqual(inventory.heaviest(), Item("anvil", 9))
        self.assertIsNone(Inventory().heaviest())

    # def test_equal_weights_are_ordered_by_name(self):
    #     inventory = Inventory([("cup", 3), ("anvil", 9), ("book", 3), ("ant", 3)])
    #     expected = "????"
    #     self.assertEqual([item.name for item in inventory.items_by_weight()], expected)

    # def test_heaviest_breaks_ties_by_name(self):
    #     inventory = Inventory([("zebra", 5), ("apple", 5)])
    #     expected = "????"
    #     self.assertEqual(inventory.heaviest().name, expected)


if __name__ == "__main__":
    unittest.main()
