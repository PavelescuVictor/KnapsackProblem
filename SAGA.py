from Classes.Backpack import Backpack
from Classes.Item import Item
from Classes.Table import Table

import Utility
from datetime import datetime

import time

import operator
import random
import copy

class SAGA:

    def __init__(self):
        self.backpack = Backpack()
        self.table = Table('')

    def main_menu(self):
        print("\n0.Exit program.")
        print("1.Read from file.")
        print("2.Read from keyboard.")
        print("3.Check if random generated solution is valid.")
        print("4.Best out of k solutions randomly generated.")
        print("5.Steepest ascent hill-climbing (SAHC).")
        print("6.Genetic algorithm.")

    def read_from_file(self, file_name):
        try:
            file = open(file_name, "r")
        except :
            print("There is no file %s" % file_name)
        else:
            file_content = file.read().splitlines()
            size = file_content[0]
            max_weight = file_content[len(file_content) - 1]
            self.backpack = Backpack()
            self.backpack.set_max_weight(max_weight)
            for i in range(1, int(size) + 1):
                line_content = list(map(int, file_content[i].split()))
                value = line_content[1]
                weight = line_content[2]
                item = Item(value, weight)
                self.backpack.add_item(item)
            file.close()

    def solution_sum(self, solution):
        index = 0
        total_sum = 0
        for digit in solution:
            if int(digit) == 1:
                value = self.backpack.get_element_by_index(index).get_value()
                total_sum = total_sum + value
            index = index + 1
        return total_sum

    def solution_weight(self, solution):
        index = 0
        total_weight = 0
        for digit in solution:
            if int(digit) == 1:
                weight = self.backpack.get_element_by_index(index).get_weight()
                total_weight = total_weight + weight
            index = index + 1
        return total_weight

    def check_if_valid_solution(self, solution):
        total_weight = self.solution_weight(solution)
        if total_weight <= int(self.backpack.get_max_weight()):
            return 1
        else:
            return 0

    def generate_k_solutions(self, number_solutions):
        # Creating the file name
        file_name = str(datetime.now())[:-7]
        file_name = file_name.replace(":", "-")

        # Create an instance of the Table class using file_name
        self.table = Table(file_name)

        # Defined worksheet column 0 proprieties
        self.table.set_column_width(0, 30)

        # Defined cell proprieties
        cell_format = self.table.set_cell_proprieties()

        # Writing data in the cells
        # Column A
        self.table.insert_in_specified_column(0, "Objects", cell_format)
        for i in self.backpack.get_backpack():
            self.table.insert_in_specified_column(0, "Object {}  Value: {}  Weight: {}".format(
                self.backpack.get_backpack().index(i) + 1, i.get_value(), i.get_weight()
            ), cell_format)
        self.table.insert_in_specified_column(0, "Total Value:", cell_format)
        self.table.insert_in_specified_column(0, "Total Weight({}):".format(
            self.backpack.get_max_weight()
        ), cell_format)
        self.table.insert_in_specified_column(0, "Is Valid:", cell_format)
        if number_solutions > 1:
            self.table.insert_in_specified_column(0, "Best Solution:", cell_format)
            self.table.insert_in_specified_column(0, "Avg Solution:", cell_format)
        self.table.set_row_index()

        # Columns B,C...
        insert_token = True
        column_number = 1
        while insert_token == True:
            self.table.insert_in_specified_column(column_number, "Rnd Gen Sol {}".format(column_number), cell_format)
            # Generating a solution
            binary_random_value = Utility.generate_random_value(len(self.backpack.get_backpack()))
            # Populate table at column column_number (If a digit in the solution is 1 then the object
            # is in the backpack else the object is not
            for digit in binary_random_value:
                if int(digit) == 1:
                    self.table.insert_in_specified_column(column_number, "In", cell_format)
                else:
                    self.table.insert_in_specified_column(column_number, "Out", cell_format)
            # Check if the solution is valid
            response = self.check_if_valid_solution(binary_random_value)
            # Get total_sum and total_weight of the solution
            total_sum = self.solution_sum(binary_random_value)
            total_weight = self.solution_weight(binary_random_value)
            # If the solution is valid then insert in table
            if int(response) == 1:
                self.table.insert_in_specified_column(column_number, total_sum, cell_format)
                self.table.insert_in_specified_column(column_number, total_weight, cell_format)
                self.table.insert_in_specified_column(column_number, "Yes", cell_format)
                self.table.update_best_solution(total_sum, total_weight)
                self.table.update_avg_solution(total_sum, total_weight)
                column_number = column_number + 1
            # Resetting the row index back to 0
            self.table.set_row_index()
            self.table.set_column_width(column_number, 24)
            if column_number > number_solutions:
                insert_token = False

    def best_out_of_k_solutions(self, number_solutions):
        self.generate_k_solutions(number_solutions)
        if number_solutions > 1:
            self.table.merge_cells(
                len(self.backpack.get_backpack()) + 4, 1, len(self.backpack.get_backpack()) + 4, number_solutions)
            self.table.merge_cells(
                len(self.backpack.get_backpack()) + 5, 1, len(self.backpack.get_backpack()) + 5, number_solutions)
            best_solution_sum, best_solution_weight = self.table.get_best_solution()
            avg_solution_sum, avg_solution_weight = self.table.get_avg_solution()
            avg_solution_sum = avg_solution_sum / number_solutions
            avg_solution_weight = avg_solution_weight / number_solutions
            self.table.insert_in_specified_cell(
                len(self.backpack.get_backpack()) + 4, 1, "Value: {}        Weight: {}".format(
                    best_solution_sum, best_solution_weight
                ))
            self.table.insert_in_specified_cell(
                len(self.backpack.get_backpack()) + 5, 1, "Value: {}        Weight: {}".format(
                    avg_solution_sum, avg_solution_weight
                ))
        self.table.close_workbook()

    def determine_better_solution(self, solution1, solution2):
        total_sum1 = self.solution_sum(solution1)
        total_sum2 = self.solution_sum(solution2)
        if total_sum1 > total_sum2:
            return solution1
        else:
            return solution2

    def best_neighbour(self, solution):
        index = 0
        best_neighbour = solution
        for digit in solution:
            if digit == "0":
                neighbour = solution[:index] + '1' + solution[index + 1:]
                response = self.check_if_valid_solution(neighbour)
                if response == 1 and self.solution_sum(neighbour) > self.solution_sum(best_neighbour):
                    best_neighbour = neighbour
            index = index + 1
        if best_neighbour == solution:
            return ''
        else:
            return best_neighbour


    def steepest_ascent_hill_climbing(self, number_eval, best, all_iteration):
        #print("Main iteration : {}".format(all_iteration))
        if all_iteration < number_eval:
            #print("Best solution: {} -- Sum: {} -- Weight: {}".format(best, self.solution_sum(best), self.solution_weight(best)))
            binary_random_value = Utility.generate_random_value(len(self.backpack.get_backpack()))
            #print("Rnd gen val: {} -- Sum: {} -- Weight: {}".format(binary_random_value, self.solution_sum(binary_random_value), self.solution_weight(binary_random_value)))
            response = self.check_if_valid_solution(binary_random_value)
            if response == 1:
                index_iteration = 1
                loop_token = True
                while(loop_token == True):
                    best_neighbour = self.best_neighbour(binary_random_value)
                    if best_neighbour == '':
                        #print("Solution: {} -- Sum: {} -- Weight: {}".format(binary_random_value, self.solution_sum(binary_random_value), self.solution_weight(binary_random_value)))
                        if self.solution_sum(binary_random_value) > self.solution_sum(best):
                            best = binary_random_value
                        loop_token = False
                        self.steepest_ascent_hill_climbing(number_eval, best, all_iteration + index_iteration)
                    else:
                        #print("Iteration: {} -- Best neighbour: {} -- Sum: {} -- Weight: {}".format(index_iteration, best_neighbour, self.solution_sum(best_neighbour), self.solution_weight(best_neighbour)))
                        binary_random_value = best_neighbour
                        index_iteration = index_iteration + 1
                #print(binary_random_value,"--",self.solution_sum(binary_random_value),"--",self.solution_weight(binary_random_value))
            else:
                self.steepest_ascent_hill_climbing(number_eval, best, all_iteration)
        else:
            print("finished")
            print("best: {} -- sum: {} -- weight: {}".format(best, self.solution_sum(best), self.solution_weight(best)))

    def genetic_algorithm_initialization(self, population_size, number_generations, crossover_prob, mutation_prob):
        # Population initialization

        population_pool = []
        for i in range(0, population_size):
            binary_random_value = Utility.generate_random_value(len(self.backpack.get_backpack()))
            population_pool.append(binary_random_value)

        # Accepted chromosomes

        accepted_pool = []
        index = 0
        for i in population_pool:
            valid_token = self.check_if_valid_solution(i)
            if valid_token == 1:
                accepted_pool.append((index + 1, i))
            else:
                accepted_pool.append((index + 1, 0))
            index = index + 1

        index_generations = 1

        # Generations
        self.genetic_algorithm(population_size, index_generations, number_generations, accepted_pool, population_pool, crossover_prob, mutation_prob)

    def genetic_algorithm(self, population_size, index_generations, number_generations, accepted_pool, population_pool, crossover_prob, mutation_prob):

        if index_generations != number_generations + 1:

            # Roulette wheel selection
            '''
            print()
            print("Accepted Pool")
            for i in accepted_pool:
                print(i)
            print()
            '''
            ordered_accepted_pool = [i for i in accepted_pool if i[1] != 0]
            ordered_accepted_pool = sorted(ordered_accepted_pool, key=lambda tup: self.solution_sum(tup[1]), reverse=True)
            '''
            print()
            print("Ordered Accepted Pool")
            for i in ordered_accepted_pool:
                print(i)
            print()
            '''
            # Calculate fitness sum
            fsum = 0
            for i in ordered_accepted_pool:
                fsum += self.solution_sum(i[1])

            # Calculate fitness wieght
            fweight = 0
            for i in ordered_accepted_pool:
                fweight += self.solution_weight(i[1])

            # Roulette wheel selection with fitness
            roulette_wheel = []
            for i in range(len(ordered_accepted_pool)):
                new = (ordered_accepted_pool[i][0], self.solution_sum(ordered_accepted_pool[i][1]) / fsum)
                roulette_wheel.append(new)

            # Selection process
            selection = []
            for i in range(0, population_size):
                rand_value = random.uniform(roulette_wheel[len(roulette_wheel) - 1][1], roulette_wheel[0][1])
                for j in range(len(roulette_wheel) - 1, -1, -1):
                    if rand_value <= roulette_wheel[j][1]:
                        selection.append(roulette_wheel[j])
                        break

            '''
            print()
            print("Selection")
            for i in selection:
                print(i)
            print()
            '''
            # Selection process with chromosomes
            selection_chromosome = []
            for i in selection:
                selection_chromosome.append((i[0], population_pool[i[0] - 1]))
            '''
            print()
            print("Selection Sum")
            for i in selection_chromosome:
                print(i)
            print()
            '''
            # Selection_
            ordered_selection_chromosome= sorted(selection_chromosome, key=lambda tup: self.solution_sum(tup[1]), reverse = True)
            '''
            print()
            print("Ordered Selection Chromosome")
            for i in ordered_selection_chromosome:
                print(i)
            print()
            '''
            '''
            # Crossover
            crossover_pool = []
            chromosome_size = len(self.backpack.get_backpack())
            mutation_index = round(random.uniform(1, chromosome_size))
            for i in range(0, len(ordered_selection_chromosome) - 1, + 2):
                first_strip = ordered_selection_chromosome[i][1][-mutation_index:]
                second_strip = ordered_selection_chromosome[i + 1][1][-mutation_index:]
                first_new_chromosome = ordered_selection_chromosome[i][1][:chromosome_size - mutation_index] + second_strip
                second_new_chromosome = ordered_selection_chromosome[i + 1][1][:chromosome_size - mutation_index] + first_strip
                crossover_pool.append((i + 1, first_new_chromosome))
                crossover_pool.append((i + 2, second_new_chromosome))
            '''
            # Crossover with probability
            crossover_pool = []
            chromosome_size = len(self.backpack.get_backpack())
            for i in range(0, len(ordered_selection_chromosome) - 1, + 2):
                parent1 = ordered_selection_chromosome[i][1]
                parent2 = ordered_selection_chromosome[i + 1][1]
                child1 = ''
                child2 = ''
                for j in range(0, chromosome_size):
                    random_prob = round(random.uniform(0, 100))
                    if random_prob <= (100 - crossover_prob):
                        child1 = child1 + parent2[j]
                        child2 = child2 + parent1[j]
                    elif random_prob <= 100 and random_prob > 20:
                        child1 = child1 + parent1[j]
                        child2 = child2 + parent2[j]
                crossover_pool.append((i + 1, child1))
                crossover_pool.append((i + 2, child2))
            '''
            print()
            print("Crossover_pool")
            for i in crossover_pool:
                print(i)
            print()
            '''
            # Mutation
            mutation_pool = []
            chromosome_size = len(self.backpack.get_backpack())
            for i in range(0, len(crossover_pool)):
                child = crossover_pool[i][1]
                mutated_child = ''
                for j in range(0, chromosome_size):
                    random_prob = round(random.uniform(0, 100))
                    if random_prob <= mutation_prob:
                        if child[j] == '1':
                            mutated_child = mutated_child + '0'
                        else:
                            mutated_child = mutated_child + '1'
                    elif random_prob > mutation_prob:
                        mutated_child = mutated_child + child[j]
                mutation_pool.append((i + 1, mutated_child))
            '''
            print()
            print("Mutated Pool")
            for i in mutation_pool:
                print(i)
            print()
            '''

            # Accepting mutated pool
            accepted_mutation_pool = []
            index = 0
            for i in mutation_pool:
                valid_token = self.check_if_valid_solution(i[1])
                if valid_token == 1:
                    accepted_mutation_pool.append((index + 1, i[1]))
                else:
                    accepted_mutation_pool.append((index + 1, 0))
                index = index + 1

            ordered_accepted_mutation_pool = [i for i in accepted_mutation_pool if i[1] != 0]
            ordered_accepted_mutation_pool = sorted(ordered_accepted_mutation_pool, key=lambda tup: self.solution_sum(tup[1]), reverse=True)
            '''
            print()
            print("Ordered Accepted Mutation Pool")
            for i in ordered_accepted_mutation_pool:
                print(i)
            print()
            '''
            # Calculate fitness sum for mutated
            fmsum = 0
            for i in ordered_accepted_mutation_pool:
                fmsum += self.solution_sum(i[1])

            # Calculate fitness wieght for mutated
            fmweight = 0
            for i in ordered_accepted_mutation_pool:
                fmweight += self.solution_weight(i[1])

            # Roulette wheel selection with fitness for mutated
            roulette_wheel_ordered_mutated_pool = []
            for i in range(len(ordered_accepted_mutation_pool)):
                new = (ordered_accepted_mutation_pool[i][0], self.solution_sum(ordered_accepted_mutation_pool[i][1]) / fsum)
                roulette_wheel_ordered_mutated_pool.append(new)
            '''
            print()
            print("Roulette Wheel Ordered Accepted Mutation Pool")
            for i in roulette_wheel_ordered_mutated_pool:
                print(i)
            print()
            '''
            # Selection process for mutated
            selection_mutated = []
            for i in range(0, population_size):
                rand_value = random.uniform(roulette_wheel_ordered_mutated_pool[len(roulette_wheel_ordered_mutated_pool) - 1][1], roulette_wheel_ordered_mutated_pool[0][1])
                for j in range(len(roulette_wheel_ordered_mutated_pool) - 1, -1, -1):
                    if rand_value <= roulette_wheel_ordered_mutated_pool[j][1]:
                        selection_mutated.append(roulette_wheel_ordered_mutated_pool[j])
                        break
            '''
            print()
            print("Selection mutated")
            for i in selection_mutated:
                print(i)
            print()
            '''
            selection_mutated_chromosome = []
            for i in selection_mutated:
                selection_mutated_chromosome.append((i[0], accepted_mutation_pool[i[0] - 1][1]))
            '''
            print()
            print("Selected Mutated Chromosome")
            for i in selection_mutated_chromosome:
                print(i)
            print()
            '''
            # Printing
            print("Generations: {}".format(index_generations))
            print("Generation interval:[{},{}]".format(roulette_wheel[len(roulette_wheel) - 1][1], roulette_wheel[0][1]))

            avg_sum = 0
            for i in selection_mutated_chromosome:
                avg_sum += self.solution_sum(i[1])
            avg_sum = avg_sum / population_size

            avg_weight = 0
            for i in selection_mutated_chromosome:
                avg_weight += self.solution_weight(i[1])
            avg_weight = avg_weight / population_size

            print("Start avg sum: {}".format(fsum / len(ordered_accepted_pool)))
            print("Start avg weight: {}".format(fweight/ len(ordered_accepted_pool)))
            print("Start best sum: {}".format(self.solution_sum(ordered_accepted_pool[0][1])))
            print("Start best weight: {}".format(self.solution_weight(ordered_accepted_pool[0][1])))
            print("End avg sum: {}".format(avg_sum))
            print("End avg weight: {}". format(avg_weight))
            print('')

            self.genetic_algorithm(population_size, index_generations + 1, number_generations, selection_mutated_chromosome, population_pool, crossover_prob, mutation_prob)
        else:
            print("Stopped.")
