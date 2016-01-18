#!/usr/bin/env python3.4

import json
#from pprint import pprint
import sys

def get_food_places():
    """Prints all of the Yelp business categories that represet restaurants and
    food places"""
    #food_set = set()
    categories = ""

    with open("assets/categories.json") as filename:
        json_data = json.load(filename)

    for d in json_data:
        try:
            parents = d["parents"]
            if "food" in parents or "restaurants" in parents:
                categories = "\n".join((categories, d["title"], d["alias"]))
                #food_set.add(d["title"])
                #food_set.add(d["alias"])
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            #pprint(d)
            sys.exit(1)

    print(categories)

if __name__ == "__main__":
    get_food_places()
