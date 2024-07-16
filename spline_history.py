from spline import Spline

from typing import List

class SplineHistory():
    spline_list = []
    actual_index = -1
    max_length = 30
    
    def add_spline(self, spl, cur_knot_ind):
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
        return self.spline_list[index][0].copy()
    
    def copy_cur_knot_ind(self, index):
        return self.spline_list[index][1]