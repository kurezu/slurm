from typing import List

class SplineHistory():
    '''Класс для сохранения последних изменений сплайна. Колчество сохранений указано в параметре max_lenght'''
    spline_list = []
    actual_index = -1
    max_length = 30
    
    def add_spline(self, spl, cur_knot_ind):
        '''Метод для добавления акутального сплайна и активного узла в список для сохранения действий'''
        self.spl_copy = spl[:]

        if self.actual_index != len(self.spline_list) - 1:
            self.spline_list = self.spline_list[:self.actual_index + 1]
            self.actual_index = len(self.spline_list) - 1
        
        self.spline_list.append([self.spl_copy, cur_knot_ind])
        self.actual_index += 1
        if len(self.spline_list) > self.max_length:
            self.spline_list = self.spline_list[1:]
            self.actual_index = len(self.spline_list) - 1
    
    def copy_spline(self, index):
        '''Метод для получения спалйна по заданному индексу из сохраненного списка'''
        return self.spline_list[index][0].copy()
    
    def copy_cur_knot_ind(self, index):
        '''Метод для получения активного узла по заданному индексу из сохраненного списка'''
        return self.spline_list[index][1]