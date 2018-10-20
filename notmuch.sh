#!/bin/bash
#
# PowerStatus10k segment.
# This segment displays the current mail status by notmuch.


# Format the given information into the string with icons.
#
function formatState {
  echo "${NOTMUCH_ICON_MESSAGES} $1 ${NOTMUCH_ICON_SEPARATOR} ${NOTMUCH_ICON_ACCOUNTS} $2"
}

# Interface

# Implement the interface function for the initial subscription state.
#
function initState_notmuch {
  # Trigger hook for first time to get current state.
  $(dirname ${BASH_SOURCE[0]})/notmuch_hook.py &
  STATE="$(formatState 0 0)"
}

# Implement the interface function to format the current state of the subscription.
#
function format_notmuch {
  IFS=' ' read -ra numbers <<< "$1"
  messages="${numbers[0]}"
  accounts="${numbers[1]}"
  eval "state=\$(formatState ${messages} ${accounts})"
  STATE="$state"
}
