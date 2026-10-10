'''The rules of the guide: how your evidence narrows down the ghost.

Nothing in this file draws a window. Every function takes plain Python data
and gives plain Python data back, so the same rules work in the desktop app,
in a Jupyter notebook, and later on a web page.
'''


# The three choices you can make for each piece of evidence.
RULED_OUT = 'Ruled Out'
UNKNOWN = 'Unknown'
FOUND = 'Found'
EVIDENCE_CHOICES = [RULED_OUT, UNKNOWN, FOUND]

# Every possible result for a ghost, from most likely to eliminated.
CONFIRMED = 'Confirmed'
TWO_FOUND = 'Two Found'
ONE_FOUND = 'One Found'
OPEN = 'Open'
ELIMINATED = 'Eliminated'


def get_evidence_types(ghosts):
    '''Return every kind of evidence used by any ghost, in alphabetical order.'''
    evidence_types = []
    for ghost in ghosts:
        for evidence in ghost['evidence']:
            if evidence not in evidence_types:
                evidence_types.append(evidence)
    return sorted(evidence_types)


def new_selections(evidence_types):
    '''Return a fresh set of choices with every piece of evidence set to Unknown.'''
    selections = {}
    for evidence in evidence_types:
        selections[evidence] = UNKNOWN
    return selections


def ghost_status(ghost, selections):
    '''Decide how well a ghost matches the evidence you have marked.

    A ghost is eliminated when either of these is true:
        you ruled out a piece of evidence this ghost always leaves, or
        you found a piece of evidence this ghost never leaves.

    Otherwise the result depends on how many of its three pieces you found.
    '''
    found_count = 0

    for evidence, choice in selections.items():
        ghost_has_it = evidence in ghost['evidence']

        if choice == RULED_OUT and ghost_has_it:
            return ELIMINATED
        if choice == FOUND and not ghost_has_it:
            return ELIMINATED
        if choice == FOUND and ghost_has_it:
            found_count += 1

    if found_count == 3:
        return CONFIRMED
    if found_count == 2:
        return TWO_FOUND
    if found_count == 1:
        return ONE_FOUND
    return OPEN


def remaining_evidence(ghost, selections):
    '''Return the evidence this ghost leaves that you have not marked yet.

    When a ghost has two pieces found, this is the one thing left to look for.
    '''
    remaining = []
    for evidence in ghost['evidence']:
        if selections.get(evidence, UNKNOWN) == UNKNOWN:
            remaining.append(evidence)
    return remaining


def summarize(ghosts, selections):
    '''Return a dictionary of each ghost's name and its current result.

    Handy in a notebook for checking the rules without opening the window.
    '''
    results = {}
    for ghost in ghosts:
        results[ghost['name']] = ghost_status(ghost, selections)
    return results


def format_time(total_seconds):
    '''Turn a number of seconds into a clock reading such as 0:02:00.'''
    hours, leftover = divmod(total_seconds, 3600)
    minutes, seconds = divmod(leftover, 60)
    return f'{hours}:{minutes:02d}:{seconds:02d}'
