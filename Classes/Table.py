# pip install XlsxWriter (for installing XlsxWriter
import xlsxwriter


class Table:

    def __init__(self, file_name):
        self.out_workbook = xlsxwriter.Workbook('{}.xlsx'.format(file_name))
        self.out_sheet = self.out_workbook.add_worksheet()
        self.best_solution_sum = 0
        self.best_solution_weight = 0
        self.avg_solution_sum = 0
        self.avg_solution_weight = 0
        self.indexR = 0

    def update_best_solution(self, total_sum, total_weight):
        if total_sum > self.best_solution_sum:
            self.best_solution_sum = total_sum
            self.best_solution_weight = total_weight

    def update_avg_solution(self, total_sum, total_weight):
        self.avg_solution_weight = self.avg_solution_weight + total_weight
        self.avg_solution_sum = self.avg_solution_sum + total_sum

    def set_column_width(self, indexC, width):
        self.out_sheet.set_column(indexC, indexC, width)

    def set_cell_proprieties(self):
        cell_format = self.out_workbook.add_format()
        cell_format.set_center_across()
        return cell_format

    def set_row_index(self):
        self.indexR = 0

    def get_best_solution(self):
        return self.best_solution_sum, self.best_solution_weight

    def get_avg_solution(self):
        return self.avg_solution_sum, self.avg_solution_weight

    def merge_cells(self, indexR1, indexC1, indexR2, indexC2):
        self.out_sheet.merge_range(
            indexR1, indexC1, indexR2, indexC2, ''
        )

    def insert_in_specified_column(self, indexC, data, cell_format):
        self.out_sheet.write(self.indexR, indexC, data, cell_format)
        self.indexR = self.indexR + 1

    def insert_in_specified_cell(self, indexR, indexC, data):
        self.out_sheet.write(indexR, indexC, data)

    def close_workbook(self):
        self.out_workbook.close()
