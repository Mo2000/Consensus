# Consensus
Dragon Hacks 2016 Project

# Description
View the project page at https://mo2000.github.io/Consensus/
View the Devpost Submission at http://devpost.com/software/consensus

# Requirements
1. Two Yelp users with previously written reviews
2. Download the RSS feeds for the two users locally from http://www.yelp.com/rss
3. Python 3.4 or greater

# Usage
./consensus.py person1_rss.xml person2_rss.xml

The output will contain the favorite food types and favorite restaurants the two people have in common
The output will be printed on the command line

# Future Ideas
1. Create a web front end to showcase the results
2. Incorporate a method to automatically retrieve the users' previously written reviews via RSS
3. Incorporate restaurant price
4. Add Instagram support by using the IBM Watson Alchemy AI toolkit
5. Enhance the list of favorite food types in common by adding a threshold to show only the most liked ones
6. Enhance the restaurant recommendation by using a more complex method
