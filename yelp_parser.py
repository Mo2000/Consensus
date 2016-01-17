#!/usr/bin/env python3.4

import traceback
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
import yelp_business
import watson
from pprint import pprint
import sys

HELP_MSG = """Usage:
./yelp_sentiment.py yelp_reviews.xml
"""


def parse_xml(xml_file):
    """Given a path to an XML file, return the root XML ElementTree object"""
    return ET.parse(xml_file)


def parse_user(xml_tree):
    """Given the root XML ElementTree object, parse and return the Yelp
    username as a string"""
    if xml_tree is None:
        return None
    title = xml_tree.find("./channel/title").text
    user = " ".join(title.split()[:-2]) # remove the "on Yelp" text
    return user


def parse_reviews(xml_tree):
    """Given the root XML ElementTree object, parse and yield a pair containing
    the yelp_id and the review left by the user"""
    if xml_tree is None:
        raise ValueError("XML tree is None. Cannot parse reviews")
    for review in xml_tree.findall("./channel/item"):
        link = review.find("link").text
        business_id = parse_business_id(link)
        business_cats_set = buss_food_cats(business_id)
        if business_cats_set:
            desc = review.find("description").text
            yield business_id, business_cats_set, desc


def parse_business_id(url_link):
    """This is a helper function. Given a text containing the Yelp URL of a
    restaurant, return the portion containing the Yelp ID of the
    restaurant"""
    result = urlsplit(url_link)
    business_id = result.path.split("/")[2]
    return business_id


def read_categories():
    """Returns a set containing all of the parsed categories"""
    return set(line.strip() for line in open("assets/categories.txt"))


def buss_food_cats(business_id):
    """Given a Yelp business ID, compare the business categories with those of
    food places on Yelp. If the intersection of the business categories and the
    food place categories is not an empty set, then return it. Else, return
    None"""
    categories_set = read_categories()
    business_set = yelp_business.get_categories(business_id)
    intersection = categories_set & business_set
    if intersection:
        return intersection
    return None


def parse_emotions_dict(emotions_dict):
    """Given a dictionary containing the emotional sentiment of the Yelp
    review, return a pipe separated string of the percentages of the
    three emotions in the following order:
    anger_percentage|negative_percentage|cheerfulness_percentage"""
    anger_p = str(emotions_dict["Anger"]["percentage"])
    negative_p = str(emotions_dict["Negative"]["percentage"])
    cheerfulness_p = str(emotions_dict["Cheerfulness"]["percentage"])
    return "|".join((anger_p, negative_p, cheerfulness_p))


def parse_unique_food_types(food_category_set):
    """Given a set containing the food types of the business that was reviewed
    on Yelp, return a string containing unique food types in a pipe separated
    format. Example output:
    japanese|middle eastern|italian"""
    l = [e.lower() for e in food_category_set]
    return "|".join(set(l))


def text_output_generator(tree):
    """Given the directory to the XML file containing the Yelp reviews for a
    user, yields the output in pipe generated text format. Example:
    yelp_business_id|anger_%|negative_%|cheerfulness_%|food_categories"""
    for business_id, business_cats_set, desc in parse_reviews(tree):
        response_dict = watson.query_watson(desc)
        emotions_dict = watson.gen_emotions_dict(response_dict)
        yield business_id, business_cats_set, emotions_dict
        #emotions = parse_emotions_dict(emotions_dict)
        #food_types = parse_unique_food_types(business_cats_set)
        #output = "|".join((business_id, emotions, food_types))
        #yield output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(HELP_MSG)
        sys.exit(1)

    try:
        tree = parse_xml(sys.argv[1])
        for output in text_output_generator(tree):
            print(output)
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        sys.exit(1)
