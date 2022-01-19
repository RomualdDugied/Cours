#!/usr/bin/python3.8
# -*-coding:utf-8 -*-

#dataset
#Customer Order list
#Order : [state, id, name of customer]
#state : 1 = Received; 2 = Prepared; 3 = Shipped; 4 = Completed
The_list = [[1, 2100, "Dupont"],
            [4, 2101, "Durand"],
            [3, 2102, "Robert"],
            [4, 2103, "Gros"],
            [4, 2104, "Léger"],
            [2, 2105, "Terreau"]
            ]

ORDER_STATE = 0
ORDER_ID = 1
ORDER_CUSTOMER_NAME = 2

RECEIVED_ORDER = 1
PREPARED_ORDER = 2
SHIPPED_ORDER = 3
COMPLETED_ORDER = 4

def get_completed_orders(selected_orders: list) -> list:
    completed_orders = list()

    for order in selected_orders:
        if order[ORDER_STATE] == COMPLETED_ORDER:
            completed_orders.append(order)

    return completed_orders



if __name__ == "__main__":
    print(get_completed_orders(The_list))
