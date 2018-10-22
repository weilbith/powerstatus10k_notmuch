#!/bin/bash
#
# PowerStatus10k segment.
# This segment displays the current mail status by notmuch.


# Format the given information into the string with icons.
# Set the highlight color if given.
#
# Arguments:
#   $1 - number of unread messages
#   $2 - number of different addresses
#   $3 - color to highlight (optional)
#
function formatState {
  formatString="${NOTMUCH_ICON_MESSAGES} $1 ${NOTMUCH_ICON_SEPARATOR} ${NOTMUCH_ICON_ADDRESSES} $2"

  [[ -n "$3" ]] && formatString="%{F${3}}${formatString}%{F-}"

  echo "$formatString"
}


# Segment Interface

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
  IFS=' ' read -ra status <<< "$1"
  messages="${status[0]}"
  accounts="${status[1]}"
  color="${status[2]}"
  eval "state=\$(formatState \"${messages}\" \"${accounts}\" \"${color}\")"
  STATE="$state"
}
