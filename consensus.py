#!/usr/bin/env python3.4

from yelp_parser import text_output_generator, parse_user, parse_xml
import traceback

HELP_MSG = """Usage:
./consensus.py person1_yelp_reviews.xml person2_yelp_reviews.xml
"""

class person:
    """A class to hold a person's name, favorite cuisines, and the businesses
    he/she has reviewed on Yelp"""
    def __init__(self, name):
        self.name = name
        self.businesses = {}
        self.cuisines = set()

    def update_businesses(self, business_id, business_categories_set, metrics_dict):
        """Given a Yelp business ID, a set containing Yelp categories of the
        business, and a dictionary containing the emotional sentiment of their
        review, update the person class object to hold the newly supplied
        information"""
        self.businesses[business_id] = {}
        self.businesses[business_id]["categories"] = business_categories_set
        self.businesses[business_id]["metrics"] = metrics_dict
        self.cuisines = self.cuisines | business_categories_set


def cuisines_in_common(person1, person2):
    """Given two person class objects, return the set intersection between
    their favorite cuisines"""
    return person1.cuisines & person2.cuisines


def find_max_cheer(person):
    """Given a person class object, return the max percentage for the
    cheerfulness emotional tone in all of their business reviews"""
    max_percent = 0
    for busn in person.businesses:
        temp = person.businesses[busn]["metrics"]["Cheerfulness"]["percentage"]
        if temp > max_percent:
            max_percent = temp
    return max_percent


def find_restaurants(max_percent, person):
    """Given a max percentage and a person class object, return a set
    containing all of the businesses that have had the same percentage
    value for the cheerfulness emotional tone"""
    s = set()
    for busn in person.businesses:
        temp = person.businesses[busn]["metrics"]["Cheerfulness"]["percentage"]
        if temp == max_percent:
            s.add(busn)
    return s


def favored_restaurants(person1, person2):
    """Given two person class objects, return the set intersection between
    their favorite restaurants"""
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
