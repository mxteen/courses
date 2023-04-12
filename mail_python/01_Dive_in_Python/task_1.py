import sys

digit_string = sys.argv[1]

s = sum([int(d) for d in digit_string])
print(s)