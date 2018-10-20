#!/usr/bin/python

# Imports
import os
import notmuch
from email.utils import parseaddr

# Properties
fifoName = '/tmp/powerstatus_segment_notmuch'

# Query Notmuch and get the count.
query = notmuch.Query(notmuch.Database(), 'is:unread and is:inbox')

# Pipe the current state to the FIFO.
def pipe(state):
    # Create the FIFO if not exist yet.
    # Do it here, to avoid problems on a deleted FIFO during runtime.
    if not os.path.exists(fifoName):
        os.mkfifo(fifoName)

    # Write to the FIFO.
    with open(fifoName, 'w') as fifo:
        fifo.write(state)

def get_message_count():
    return query.count_messages()

def get_address_count():
    messages = query.search_messages()
    address_list = dict()

    for message in messages:
        name, address = parseaddr(message.get_header('To'))
        address_list[address] = None

    return len(address_list)


message_count = get_message_count()
address_count = get_address_count()
state = str(message_count) + ' ' + str(address_count)
pipe(state)
