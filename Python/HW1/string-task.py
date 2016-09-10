
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
#
# Example input: 'read'
# Example output: 'reading'
def verbing(s):
    if len(s) >= 3:
        if s[-3:] == "ing":
            return s + "ly"
        return s + "ing"
    return s

# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
#
# Example input: 'This dinner is not that bad!'
# Example output: 'This dinner is good!'
def not_bad(s):
    i = s.find('not')
    j = 0
    if i != -1:
        j = s.find('bad', i)
    if i != -1 and i < j:
        return s[:i] + 'good' + s[j + 3:]
    return s

# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
#
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
#
# Example input: 'abcd', 'xy'
# Example output: 'abxcdy'
def front_back(a, b):
    a_mid = (len(a) + 1) // 2
    a_front = a[:a_mid]
    a_back = a[a_mid:]

    b_mid = (len(b) + 1) // 2
    b_front = b[:b_mid]
    b_back = b[b_mid:]

    return a_front + b_front + a_back + b_back
