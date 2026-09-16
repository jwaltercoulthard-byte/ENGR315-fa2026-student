import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###

    
    #Set other variables to initial values
    a = 1
    b = 1 / math.sqrt(2)
    t = 1 / 4
    p = 1

    while (abs(a-b) >= target_error):

        a_next = (a + b) / 2
        b_next = math.sqrt(a * b)
        t_next = t - p * (a - a_next) ** 2
        p_next = 2 * p

        #update variables
        a = a_next
        b = b_next
        t = t_next
        p = p_next


    # change this so an actual value is returned
    return (a + b) ** 2 / (4 * t)



desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
