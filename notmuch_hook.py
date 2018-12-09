#!/usr/bin/python

# Imports
import os
import notmuch
from email.utils import parseaddr
from functools import reduce


class NotmuchHook:
    runtime_dir = os.getenv('XDG_RUNTIME_DIR', '/tmp') + '/powerstatus10k'
    exchange_dir = runtime_dir + '/notmuch'
    fifo_name = runtime_dir + '/fifos/notmuch'
    database = None

    # Files where to search for stored queries by the segment handler.
    unread_query_file = exchange_dir + '/unread_query'
    color_query_tuples_file = exchange_dir + '/color_query_tuples'

    unread_query = None
    color_query_tuples = None


    def __init__(self):
        self.database = notmuch.Database()

        # Read the unread query file provided by the segment handler.
        try:
            with open(self.unread_query_file, 'r') as file:
                self.unread_query = file.read()

        except:
            raise
        
        # Read the color query tuples file and parse each line provided by the segment handler.
        try:
            self.color_query_tuples = []

            with open(self.color_query_tuples_file, 'r') as file:
                for line in file.readlines():
                   self.color_query_tuples.append(line.rsplit('=', 1))

        except:
            raise


    def pipe(self, state):
        # Create the FIFO if not exist yet.
        # Do it here, to avoid problems on a deleted FIFO during runtime.
        if not os.path.exists(self.fifo_name):
            os.mkfifo(self.fifo_name)

        # Write to the FIFO.
        with open(self.fifo_name, 'w') as fifo:
            fifo.write(state)


    def unread_message_count(self):
        query = notmuch.Query(self.database, self.unread_query)
        return query.count_messages()


    def differing_address_count(self):
        messages = notmuch.Query(self.database, self.unread_query).search_messages()
        address_list = dict()

        # Count uniquely addresses by add them as keys to a mapping.
        for message in messages:
            name, address = parseaddr(message.get_header('To'))
            address_list[address] = None

        # The number of keys are the amount of individual addresses.
        return len(address_list)


    def state_color(self):
        # Check for query hits in the list.
        for query_tuple in self.color_query_tuples:
            query = self.unread_query + ' and (' + query_tuple[0] + ')'
            count = notmuch.Query(self.database, query).count_messages()

            # Stop here of any hit and return the queries color.
            if count > 0:
                return query_tuple[1]

        return ''


    def run(self):
        # Get all relevant data for the state to pipe.
        unread_count = self.unread_message_count()
        address_count = self.differing_address_count()
        color = self.state_color()
        state = reduce((lambda x, y: str(x) + ' ' + str(y)), [unread_count, address_count, color])
        self.pipe(state)


# Getting started
NotmuchHook().run()
