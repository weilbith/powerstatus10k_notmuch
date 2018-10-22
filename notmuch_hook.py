#!/usr/bin/python

# Imports
import os
import notmuch
from email.utils import parseaddr


class NotmuchHook:
    fifoName = '/tmp/powerstatus_segment_notmuch'
    query = None

    def __init__(self):
        self.query = notmuch.Query(notmuch.Database(), 'is:unread and is:inbox')

    def pipe(self, state):
        # Create the FIFO if not exist yet.
        # Do it here, to avoid problems on a deleted FIFO during runtime.
        if not os.path.exists(self.fifoName):
            os.mkfifo(self.fifoName)

        # Write to the FIFO.
        with open(self.fifoName, 'w') as fifo:
            fifo.write(state)

    def get_message_count(self):
        return self.query.count_messages()

    def get_address_count(self):
        messages = self.query.search_messages()
        address_list = dict()

        for message in messages:
            name, address = parseaddr(message.get_header('To'))
            address_list[address] = None

        return len(address_list)

    def run(self):
        message_count = self.get_message_count()
        address_count = self.get_address_count()
        state = str(message_count) + ' ' + str(address_count)
        self.pipe(state)


# Getting started
NotmuchHook().run()
