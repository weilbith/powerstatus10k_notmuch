#!/bin/bash
#
# PowerStatus10k segment.
# This segment displays the current mail status by notmuch.


# Interface

# Implement the interface function for the initial subscription state.
#
function initState_notmuch {
  STATE="${NOTMUCH_ICON_MESSAGES} 0 ${NOTMUCH_ICON_ACCOUNTS} 0"
}

# Implement the interface function to format the current state of the subscription.
#
function format_notmuch {
  IFS=' ' read -ra numbers <<< "$1"
  messages="${numbers[0]}"
  accounts="${numbers[1]}"
  STATE="${NOTMUCH_ICON_MESSAGES} ${messages} ${NOTMUCH_ICON_ACCOUNTS} ${accounts}"
}
