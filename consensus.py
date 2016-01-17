#!/usr/bin/env python3.4

from yelp_parser import text_output_generator, parse_user, parse_xml
import traceback

HELP_MSG = """Usage:
./consensus.py person1_yelp_reviews.xml person2_yelp_reviews.xml
"""

class person:
    def __init__(self, name):
        self.name = name
        self.businesses = {}
        self.cuisines = set()

    def update_businesses(self, business_id, business_categories_set, metrics_dict):
        self.businesses[business_id] = {}
        self.businesses[business_id]["categories"] = business_categories_set
        self.businesses[business_id]["metrics"] = metrics_dict
        self.cuisines = self.cuisines | business_categories_set


def cuisines_in_common(person1, person2):
    return person1.cuisines & person2.cuisines


def find_max_cheer(person):
    max_percent = 0
    for business in person.businesses:
        temp_max = person.businesses[business]["metrics"]["Cheerfulness"]["percentage"]
        if temp_max > max_percent:
            max_percent = temp_max
    return max_percent


def find_restaurants(max_percent, person):
    s = set()
    for business in person.businesses:
        if person.businesses[business]["metrics"]["Cheerfulness"]["percentage"] == max_percent:
            s.add(business)
    return s


def favored_restaurants(person1, person2):
    s = set()
    p1_max = find_max_cheer(person1)
    p2_max = find_max_cheer(person2)
    p1_res = find_restaurants(p1_max, person1)
    p2_res = find_restaurants(p2_max, person2)
    return p1_res & p2_res


if __name__ == "__main__":
    import sys
    from pprint import pprint
    
    if len(sys.argv) != 3:
        print(HELP_MSG)
        sys.exit(1)

    try:
        persons = []
        for xml in sys.argv[1:]:
            tree = parse_xml(xml)
            user_name = parse_user(tree)
            user = person(user_name)
            persons.append(user)
            for business_id, business_cats, emotions_dict \
                                                        in text_output_generator(tree):
                user.update_businesses(business_id, business_cats, emotions_dict)
            
        print("Cuisines in common between Bob and Tom:\n")
        print(cuisines_in_common(persons[0], persons[1]))
        print()
        print("Favorite restaurants in common between Bobby and Tommy:\n")
        print(favored_restaurants(persons[0], persons[1]))
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        sys.exit(1)

