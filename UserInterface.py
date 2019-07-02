from Classes.Backpack import Backpack
from Classes.Item import Item
from Classes.Table import Table
from SAGA import SAGA

import Utility
from datetime import datetime

import time

import operator
import random
import copy

class App:

    def __init__(self):
        self.SAGA = SAGA()

    def main_menu(self):
        print("\n0.Exit program.")
        print("1.Read from file.")
        print("2.Read from keyboard.")
        print("3.Check if random generated solution is valid.")
        print("4.Best out of k solutions randomly generated.")
        print("5.Steepest ascent hill-climbing (SAHC).")
        print("6.Genetic algorithm.")

if __name__ == "__main__":
    # Create an instance of the Backpack class.
    app = App()

    loop_token = 1
    while loop_token:
        app.main_menu()
        try:
            opt = int(input('Insert number of the option choosed: '))
        except ValueError:
            print("\nThe option is not a valid number.")
        else:
            if opt == 1:
                file_name = input('Insert the name of the file (type: name.txt): ')
                if file_name[-4:] == ".txt":
                    app.SAGA.read_from_file(file_name)
                else:
                    print("The name doesn't follow the type specified (type: name.txt).")
            elif opt == 2:
                print("2")
            elif opt == 3:
                app.SAGA.best_out_of_k_solutions(1)
            elif opt == 4:
                try:
                    number_solutions = int(input('How many randomly generated solutions to check?: '))
                except ValueError:
                    print("\nThat's not a valid number.")
                else:
                    app.SAGA.best_out_of_k_solutions(number_solutions)
            elif opt == 5:
                try:
                    number_eval = int(input('How many evaluations?: '))
                except ValueError:
                    print("\nThat's not a valid number.")
                else:
                    start_time = time.time()
                    best = app.SAGA.steepest_ascent_hill_climbing(number_eval, '00000000000000000000', 0)
                    print("--- %s seconds ---" % (time.time() - start_time))
            elif opt == 6:
                start_time = time.time()
                population_size = 300
                number_generations = 500
                crossover_prob = 10
                mutation_prob = 3
                app.SAGA.genetic_algorithm_initialization(population_size, number_generations, crossover_prob, mutation_prob)
                print("--- %s seconds ---" % (time.time() - start_time))
            elif opt == 0:
                loop_token = 0
                print("\nExiting program.")
            else:
                print("\nThat is not a valid option.")
