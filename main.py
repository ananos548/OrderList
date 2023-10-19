import sys

import asyncio
from sqlalchemy import select, and_
from typing import List

from src.app.models import *
from src.database import async_session_maker


async def get_order(order_id: List[int]):
    async with async_session_maker() as session:
        query = select(Product.product_name.distinct(), Order.order_number, OrderItem.quantity, Product.id,
                       Shelf.shelf_name, ProductShelfAssociation.is_main). \
            join(Product, OrderItem.product_id == Product.id). \
            join(Order, OrderItem.order_id == Order.id). \
            join(Shelf, Product.shelves). \
            join(ProductShelfAssociation, and_(
                ProductShelfAssociation.product_id == Product.id,
                ProductShelfAssociation.shelf_id == Shelf.id)). \
            where(Order.order_number.in_(order_id))
        result = await session.execute(query)
        order_items = result.fetchall()
        shelves = {}
        product_details = {}
        is_main_dict = {}
        for product in order_items:
            product_name, order_number, quantity, product_id, shelf_name, is_main = product
            if is_main:
                if shelf_name not in shelves:
                    shelves[shelf_name] = []
                if shelf_name not in product_details:
                    product_details[shelf_name] = []

                shelves[shelf_name].append((product_name, product_id, order_number, quantity))
                product_details[shelf_name].append((product_name, product_id, quantity))
            else:
                product_info = is_main_dict.get(product_id, [])
                product_info.append({"Стеллаж": shelf_name, "product_name": product_name})
                is_main_dict[product_id] = product_info
        print(is_main_dict)
        print("=+=+=+=")
        print("Страница сборки заказов", ", ".join(map(str, order_id)))

        sorted_shelves = sorted(shelves.items())

        for k, v in sorted_shelves:
            main_shelf = k
            print('===Стеллаж ' + main_shelf)

            for value in v:
                product_name, product_id, order_number, quantity = value

                additional_shelves = []
                if product_id in is_main_dict:
                    additional_shelves = [shelf_info["Стеллаж"] for shelf_info in is_main_dict[product_id]]
                print(f'{product_name} (id={product_id})\nзаказ {order_number}, {quantity} шт')

                if additional_shelves:
                    print("доп Стеллаж:", ",".join(additional_shelves))
                print()


async def main():
    order = [int(order_id) for order_id in sys.argv[1].split(',')]
    await get_order(order)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


async def main():
    order = [int(order_id) for order_id in sys.argv[1].split(',')]
    await get_order(order)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
