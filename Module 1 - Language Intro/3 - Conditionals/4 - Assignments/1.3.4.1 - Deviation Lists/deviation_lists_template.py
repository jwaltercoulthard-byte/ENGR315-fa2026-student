"""
Given two lists, use the standard deviation function from numpy to determine
which language has the largest standard deviation. Usage will be np.std()
https://numpy.org/doc/stable/reference/generated/numpy.std.html
"""

"""
Dr. Forsyth's Code. Do Not Modify.
"""
# bring in randomness because we need it in our lives
import random
import numpy as np

# randomly sample a distribution between 20 and 100
random_length = int(random.uniform(20, 100))

# generate a random list of random length containing values up to 100
random_list_A = random.sample(range(100), random_length)

# generate a random list of random length containing values up to 100
random_list_B = random.sample(range(100), random_length)

# use the std() method from numpy to determine which list has the largest standard deviation

### YOUR CODE HERE


dev1 = np.std(random_list_A)
dev2 = np.std(random_list_B)

print(f"Standard Deviation of List A: {dev1}")
print(f"Standard Deviation of List B: {dev2}")

if dev1 > dev2:
    chosen_list = random_list_A
    print("List A has the largest standard deviation.")
else:
    chosen_list = random_list_B
    print("List B has the largest standard deviation.")

# set this variable equal to the list with the largest standard deviation
# do not modify this variable's name, you can/should adjust the contents ;)
# e.g. longest_list_is = myList
longest_list_is = chosen_list

### YOUR CODE HERE
