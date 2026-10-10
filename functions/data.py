'''Loads the ghost list that powers Tobin's Spirit Guide.

The ghosts live in ghost_data.json, which sits right beside this file.
Keeping them in their own file means you can add a ghost, fix a typo, or
change a description without touching any of the program's code.
'''

import json
from pathlib import Path


# The folder this file lives in, so the ghost list is found no matter
# which folder the guide is started from.
FUNCTIONS_FOLDER = Path(__file__).parent
DEFAULT_DATA_FILE = FUNCTIONS_FOLDER / 'ghost_data.json'


def load_ghosts(path=None):
    '''Return the list of ghosts, each one a dictionary with these keys:

        name      the ghost's name
        evidence  the three pieces of evidence it leaves behind
        strength  what makes it dangerous
        weakness  how to use it against the ghost

    Leave path empty to use the ghost list that comes with the guide.
    Pass your own file path to try out an edited copy instead.
    '''
    if path is None:
        data_file = DEFAULT_DATA_FILE
    else:
        data_file = Path(path)

    with data_file.open(encoding='utf-8') as file:
        ghosts = json.load(file)

    return ghosts
