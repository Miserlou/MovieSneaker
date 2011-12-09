from itertools import tee, combinations, ifilter

def find_chains(events,chain_length=2,max_wait=10,can_miss=5):
	"""
	Takes in a list of events and some parameters and returns valid chains.

	Events is an iterable of tuples of 3 elements: (key,start,end).

    :param events: An iterable of tuples like this: (key,start,end)
    :param chain_length: How many events in a row we want
    :param max_wait: How long we can wait between events
    :param can_miss: How much of an event we're willing to miss
    :return: A list of valid chains of events
	"""
	# Used to take into account preview length, then realized that's already
	# factored in, if we assume preview lengths for all movies average out to
	# the same length so "true film start" for the previous movie will be shifted the same.
	
	events.sort(key=lambda e:e[1]) # sort by start time
    # 0,5  4,6  4-5=-1
    valid_chains = []
	for chain in combinations(events,chain_length):
		problem = False
		seen = []
		for i in range(len(chain)):
			if chain[i][0] in seen:
				problem = True
				break
			seen.append(chain[i][0])
			interval = chain[i+1][1]-chain[i][2]
			# next one starts too early or too late
			if interval < -1*can_miss or interval > max_wait:
					problem = True 
					break
		if problem:
			continue
		else:
			valid_chains.append(chain)

	return valid_chains
