#!/usr/bin/python3.8
# -*-coding:utf-8 -*-

#dataset
#Customer Order list
#Order : [state, id, name of customer]
#state : 1 = Received; 2 = Prepared; 3 = Shipped; 4 = Paid
the_list = [[1, 2100, "Dupont"],
            [4, 2101, "Durand"],
            [3, 2102, "Robert"],
            [4, 2103, "Gros"],
            [4, 2104, "Léger"],
            [2, 2105, "Terreau"]
            ]

def get_them() -> list:
    list1 = list()

    for x in the_list:
        if x[0] == 4:
            list1.append(x)

    return list1


if __name__ == "__main__":
    print(get_them())
