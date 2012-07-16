from itertools import tee, combinations, ifilter
import datetime

import logging

#logging.basicConfig(level=logging.DEBUG)

def find_chains(events,chain_length=2,max_wait=datetime.timedelta(minutes=10),can_miss=datetime.timedelta(minutes=5)):
    """
    Takes in a list of events and some parameters and returns valid chains.

    Events is an iterable of tuples of 3 elements: (key,start,end).

    >>> find_chains([('a',0,5),('b',4,7), ('c',8,9)])
    [(('a', 0, 5), ('b', 4, 7)), (('a', 0, 5), ('c', 8, 9)), (('b', 4, 7), ('c', 8, 9))]

    :param events: An iterable of tuples like this: (key,start,end)
    :param chain_length: How many events in a row we want
    :param max_wait: How long we can wait between events
    :param can_miss: How much of an event we're willing to miss
    :return: A list of valid chains of events
    """
    # TODO: Add a few more complicated tests

    # Used to take into account preview length, then realized that's already
    # factored in, if we assume preview lengths for all movies average out to
    # the same length so "true film start" for the previous movie will be shifted the same.

    # combinations scale with the factorial, so anything over 4 is going to make for really long processing
    if chain_length > 4:
        raise Exception("Hey buddy, we don't have that much time. 4 movies at most!")
    
    events.sort(key=lambda e:e[1]) # sort by start time
    # 0,5  4,6  4-5=-1
    valid_chains = [] 
    for chain in combinations(events,chain_length):
        #logging.debug(chain):
        problem = False
        seen = []
        for i in range(chain_length):
            clean_key = chain[i][0].lower().strip() if type(chain[i][0]) is str else chain[i][0]

            # only do this check if this isn't the last item
            if i<(chain_length-1):
                interval = chain[i+1][1]-chain[i][2]
                # next one starts too early or too late
                if interval < -1*can_miss or interval > max_wait:
                        problem = True 
                        break

            if clean_key in seen: # this is a duplicate, so it's not a valid chain
                problem = True
                break
            else:
                seen.append(clean_key)

        if problem:
            continue
        else:
            valid_chains.append(chain)

    return valid_chains
