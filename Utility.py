from random import randint

def generate_random_value(number_objects):
    # Create a string of number_solutions 1's
    string_val = "1" * number_objects
    # Get the decimal value of the maximum number
    max_number = int(string_val, 2)
    # Generate random value
    random_value = randint(0, max_number)
    # Create a binary random value of length number_solutions, If the lenght is shorter add 0 to the beginning
    binary_random_value = "{:0{}b}".format(random_value, number_objects )
    return binary_random_value