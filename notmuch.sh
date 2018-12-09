#!/bin/bash
#
# PowerStatus10k segment.
# This segment displays the current mail status by notmuch.

# Properties
NAME="notmuch"
EXCHANGE_DIR="${POWERSTATUS10K_DIR_RUNTIME}/${NAME}"
UNREAD_QUERY_FILE="${EXCHANGE_DIR}/unread_query"
COLOR_QUERY_TUPLES_FILE="${EXCHANGE_DIR}/color_query_tuples"


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

# Pass the query settings to the Python hook script.
#
function writeQueries {
  # Delete possible old queries.
  rm -f "$UNREAD_QUERY_FILE"
  rm -f "$COLOR_QUERY_TUPLES_FILE"

  # Create the exchange dirctory if not already exist.
  mkdir -p "$EXCHANGE_DIR"

  # Write unread query.
  echo "$NOTMUCH_QUERY_UNREAD" >> "$UNREAD_QUERY_FILE"

  # Write color tuple rules.
  touch "$COLOR_QUERY_TUPLES_FILE" # Make sure it is at least empty.

  for tuple in "${NOTMUCH_QUERY_COLORS[@]}" ; do
    echo "${tuple}" >> "$COLOR_QUERY_TUPLES_FILE"
  done
}


# Segment Interface

# Implement the interface function for the initial subscription state.
#
function initState_notmuch {
  # Provide the queries to the hook permanently.
  writeQueries

  # Trigger hook for first time to get current state.
  "$(dirname "${BASH_SOURCE[0]}")/notmuch_hook.py" &
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
  # shellcheck disable=SC2034,SC2154
  STATE="$state"
}
