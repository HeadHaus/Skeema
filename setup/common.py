#

import os


def get_long_description(readme_loc):
    with open(os.path.join(readme_loc, 'README.md')) as f:
        long_description = f.read()
    return long_description
