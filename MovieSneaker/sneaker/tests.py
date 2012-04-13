"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

import os
import cPickle

import sneakercore

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

CHAIN_LENGTH = 3

class ParsingTest(TestCase):

    def setUp(self):
        FILENAME = 'test_parse.pkl'

        # if the file isn't there we can't do this test, so it fails
        if not os.path.exists(FILENAME):
            raise Exception("Need a test case pickle to test")

        theatre = cPickle.load(open(FILENAME))
        # this is how the pickle was derived
        # fp = FlixsterParser("94043")
        # theatre = fp.get_theatres()['theatres'][0]
        # cPickle.dump(theatre,open(FILENAME,'w'))


        showtimes = []
        for movie in theatre['movies']:
            for showtime in movie['showtimes']:
                showtimes.append((movie['name'],showtime['start'],showtime['end']))

        self.showtimes = showtimes
        self.chains = sneakercore.find_chains(showtimes,chain_length=CHAIN_LENGTH)

    def test_chains_are_correct_length(self):
        """
        Tests that the chains generated are of the correct length
        """
        for chain in self.chains:
            self.assertEqual(len(chain),CHAIN_LENGTH)


    def test_chains_contain_no_duplicates(self):
        """
        Tests that chains contain no duplicate movies
        """
        for chain in self.chains:
            movie_names = [show[0] for show in chain]
            self.assertEqual(len(movie_names),len(set(movie_names)))