"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location. If
    multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    return min(centroids,key = lambda x: distance(location,x))
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # BEGIN Question 4
    a, i, j, q=[], 0, 0, 0
    for x in restaurants:
        a += [[find_closest(restaurant_location(x),centroids),restaurant_name(x)]]
    k = group_by_first(a)
    b = [[] for x in range(len(k))]
    while j < len(k):
        i = 0
        while  i < len(k[j]):
            for q in restaurants:
                if restaurant_name(q) == k[j][i]:
                    b[j].append(q) #first list
            i = i + 1
        j = j + 1
    return b
    # END Question 4


def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""
    # BEGIN Question 5
    a, i= [], 0
    b, c= [], []
    for restaurant in cluster:
        a.append(restaurant_location(restaurant))
    while i < len(a):
        b.append(a[i][0])
        c.append(a[i][1])
        i += 1
    return [mean(b),mean(c)]

    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        m = group_by_centroid(restaurants,old_centroids)
        i = 0
        while i < len(m):
            centroids[i] = find_centroid(m[i])
            i += 1
        # END Question 6
        n += 1
    return centroids


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]#the extracted values for each restaurant in restaurants
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]#the ratings for the restaurants in restaurants

    # BEGIN Question 7
    Sxrate,Syrate = [],[]
    for s in xs:
        Sxrate.append((s-mean(xs)))
    Sxx = sum([x**2 for x in Sxrate])
    for s in ys:
        Syrate.append((s-mean(ys)))#ys是列表 列表中的元素为字典 字典的key是restaurant value是rate
    Syy = sum([y**2 for y in Syrate])
    i,Sxyrate = 0,[]
    while i < len(Sxrate):
         Sxyrate.append(Sxrate[i]*Syrate[i])
         i += 1
    Sxy = sum(Sxyrate)
    b, a, r_squared = Sxy/Sxx, mean(ys)-Sxy/Sxx*mean(xs), Sxy**2/(Sxx*Syy)  # REPLACE THIS LINE WITH YOUR SOLUTION
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)#a list of restaurants reviewed by the user
    # BEGIN Question 8
    b = {find_predictor(user,reviewed,x)[1]:find_predictor(user,reviewed,x)[0] for x in feature_fns}
    a = max(find_predictor(user,reviewed,x)[1] for x in feature_fns)
    return b[a]#return a predictor, and the value r_squared
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 9
    q = {}
    for s in restaurants:
        if s in reviewed:
            q.setdefault(restaurant_name(s),user_rating(user,restaurant_name(s)))
        else:
            q.setdefault(restaurant_name(s),predictor(s))
    return q
    #rate all return a dictionary the key is restaurant_name and the number- a mix of user ratings and predicted ratings
    # END Question 9


def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    a = []
    for s in restaurants:
        for q in restaurant_categories(s):
            if query == q:
                a.append(s)
    return a #if the query string is one of the restaurant's categories
    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [restaurant_mean_rating,
            restaurant_price,
            restaurant_num_ratings,
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)
