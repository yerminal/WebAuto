start_time = "10:00:00"

metu_username = "eXXXXXX"
metu_passw = "******"

# Your lesson list:
# Usage: [courseCode, sectionCode, categoryName]
lesson_list = [
    ['6510141', '1', 'NONTECHNICAL ELECTIVE'],
    ['6510242', '1', 'NONTECHNICAL ELECTIVE'],
    ['6510242', '2', 'NONTECHNICAL ELECTIVE']
]

"""
COURSE CATEGORIES (for selection option):

MUST
RESTRICTED ELECTIVE
FREE ELECTIVE
TECHNICAL ELECTIVE
NONTECHNICAL ELECTIVE
NOT INCLUDED

"""

# It shifts the elements of lesson_list by "shift_list_number".
# The sign of "shift_list_number" changes the direction of shift.
shift_list_number = -2


# EXAMPLE:
"""
shift_list_number = -1

lessonList = [
    ['6510242', '1', 'NONTECHNICAL ELECTIVE'],
    ['6510242', '2', 'NONTECHNICAL ELECTIVE'],
    ['6510141', '1', 'NONTECHNICAL ELECTIVE']
]
"""

"""
shift_list_number = -2

lessonList = [
    ['6510242', '2', 'NONTECHNICAL ELECTIVE'],
    ['6510141', '1', 'NONTECHNICAL ELECTIVE'],
    ['6510242', '1', 'NONTECHNICAL ELECTIVE']
]
"""
###########################################################

import collections
x  = collections.deque(lesson_list)
x.rotate(shift_list_number)
lessonList = list(x)