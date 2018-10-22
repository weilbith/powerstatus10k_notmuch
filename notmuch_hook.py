#!/usr/bin/python

# Imports
import os
import notmuch
from email.utils import parseaddr
from functools import reduce


class NotmuchHook:
    database = None
    fifoName = '/tmp/powerstatus_segment_notmuch'
    unread_query = 'is:unread and is:inbox'
    flagged_query_tuples = [] 

    def __init__(self):
        self.database = notmuch.Database()

    def pipe(self, state):
        # Create the FIFO if not exist yet.
        # Do it here, to avoid problems on a deleted FIFO during runtime.
        if not os.path.exists(self.fifoName):
            os.mkfifo(self.fifoName)

        # Write to the FIFO.
        with open(self.fifoName, 'w') as fifo:
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

    def flagged_message_color(self):
        # Check for query hits in the list.
        for query_tuple in self.flagged_query_tuples:
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
        flagged_color = self.flagged_message_color()
        state = reduce((lambda x, y: str(x) + ' ' + str(y)), [unread_count, address_count, flagged_color])
        self.pipe(state)


# Getting started
NotmuchHook().run()
