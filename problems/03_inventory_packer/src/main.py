"""Runnable demo. Try: python src/main.py"""

from inventory import Inventory
from items import get_example_items
from solver import Solver


def main():
    print("BEGIN inventory packer demo")
    inventory = Inventory(get_example_items())
    print(f"added {len(inventory)} items, total weight {inventory.total_weight()}")
    print("rejected:", inventory.add_item("ghost", 0), inventory.add_item("anvil", 2), inventory.add_item("hat", -3))
    print("heaviest first:")
    for item in inventory.items_by_weight():
        print(f"  {item.name:6} {item.weight}")
    capacity = 10
    lower_bound = -(-inventory.total_weight() // capacity)
    print(f"capacity {capacity}, lower bound on boxes: {lower_bound}")
    boxes = Solver(inventory).pack(capacity)
    print(f"packed into {len(boxes) if boxes is not None else None} boxes:")
    for index, box in enumerate(boxes or [], 1):
        weight = sum(w for n, w in get_example_items() if n in box)
        print(f"  box {index}: {box} (weight {weight})")
    print("END inventory packer demo")


if __name__ == "__main__":
    main()
