'''
'''
import functools


class multi_sudoku():
    def read_sdk(self, filename):
        '''
        This is a function used to read the sudoku file as a dictionary.
        (Written by Xinru)

        **Parameters**

            filename: *string*

        **Returns**

            file: *dictionary*
        '''
        f = open(filename, "r")
        file = {}
        number = []
        map = []
        # Skip the line before "NUMBER_START"
        for line in f:
            if line.strip() == "NUMBER_START":
                break
        for line in f:
            # Skip the line after "NUMBER_END"
            if line.strip() == "NUMBER_END":
                break
            # Generate a list of lists with information of the numbers.
            lst = []
            if line != "\n":
                for x in line.strip():
                    if x != " ":
                        lst.append(int(x))
                number.append(lst)
        # Add number to the dictionary.
        file["original_map"] = number
        # Skip the line before "MAP_START"
        for line in f:
            if line.strip() == "MAP_START":
                break
        for line in f:
            # Skip the line after "GRID STOP"
            if line.strip() == "MAP_END":
                break
            # Generate a list of lists with information of the map.
            lst = []
            if line != "\n":
                for y in line.strip().split(' '):
                    lst.append(y)
                map.append(lst)
        file['original_groups'] = {}
        for y, row in enumerate(map):
            for x, z in enumerate(row):
                if z != 'oo':
                    file['original_groups'][z] = []
        for y, row in enumerate(map):
            for x, z in enumerate(row):
                if z != 'oo':
                    file['original_groups'][z].append((x, y))
        # Close the file
        f.close()
        return file

    def load_sdk_map(self, info_dict):
        '''
        '''
        # Initialize all blank positions on the map
        info_dict['original_numbers'] = {}
        info_dict['fixed_number'] = {}
        info_dict['groups'] = {}
        info_dict['possibility'] = {}
        info_dict['sub_map'] = {}
        all_points = []
        for gp in info_dict['original_groups']:
            for pt in info_dict['original_groups'][gp]:
                all_points.append(pt)
        for apt in all_points:
            info_dict['possibility'][apt] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in range(len(info_dict['original_map'])):
            for column in range(len(info_dict['original_map'][row])):
                if info_dict['original_map'][row][column] != 0:
                    info_dict['original_numbers'][(column, row)] =\
                        info_dict['original_map'][row][column]
                    info_dict['possibility'].pop((column, row))
        info_dict['groups'] = {}
        for g in ['a', 'b', 'c', 'd', 'e']:
            info_dict['groups'][g] = {}
            info_dict['sub_map'][g] = []
            for orgrp in info_dict['original_groups']:
                if g in orgrp:
                    info_dict['groups'][g][orgrp] =\
                        info_dict['original_groups'][orgrp]
                    info_dict['sub_map'][g] +=\
                        info_dict['original_groups'][orgrp]
        return info_dict

    def sub_points(self, info_dict):
        '''
        '''
        info_dict['fixed_number'].update(info_dict['original_numbers'])
        for fp in info_dict['fixed_number']:
            if fp in info_dict['possibility']:
                info_dict['possibility'].pop(fp)
            fp_x, fp_y = fp[0], fp[1]
            for grp in info_dict['sub_map']:
                if fp in info_dict['sub_map'][grp]:
                    # Sub Row Possibilities
                    test_x = 21
                    while test_x >= 0:
                        if (test_x, fp_y) in info_dict['possibility'] and\
                                (test_x, fp_y) in info_dict['sub_map'][grp]:
                            if info_dict['fixed_number'][fp] in\
                                    info_dict['possibility'][(test_x, fp_y)]:
                                info_dict['possibility'][
                                    (test_x, fp_y)
                                ].remove(info_dict['fixed_number'][fp])
                        test_x -= 1
                    # Sub Column Possibilities
                    test_y = 21
                    while test_y >= 0:
                        if (fp_x, test_y) in info_dict['possibility'] and\
                                (fp_x, test_y) in info_dict['sub_map'][grp]:
                            if info_dict['fixed_number'][fp] in\
                                    info_dict['possibility'][(fp_x, test_y)]:
                                info_dict['possibility'][
                                    (fp_x, test_y)
                                ].remove(info_dict['fixed_number'][fp])
                        test_y -= 1
                    # Sub Group Possibilities
                    for single_gp in info_dict['groups'][grp]:
                        if fp in info_dict['groups'][grp][single_gp]:
                            for point in info_dict['groups'][grp][single_gp]:
                                if point in info_dict['possibility']:
                                    if info_dict['fixed_number'][fp] in\
                                            info_dict['possibility'][point]:
                                        info_dict['possibility'][point].remove(
                                            info_dict['fixed_number'][fp])
        info_dict['shortest'] = functools.reduce(
            lambda x, y: x if len(
                info_dict['possibility'][x]
            ) < len(info_dict['possibility'][y])
            else y, info_dict['possibility'])
        return info_dict

    def next_number(self, info_dict, next_list):
        '''
        '''
        info_dict = multi_sudoku.sub_points(self, info_dict)
        new_list = []
        for p in next_list:
            info_dict = multi_sudoku.load_sdk_map(self, info_dict)
            # print(p)
            info_dict['fixed_number'].update(p)
            info_dict = multi_sudoku.sub_points(self, info_dict)
            # print(info_dict['shortest'])
            # print(info_dict['possibility'][info_dict['shortest']])
            # print(info_dict)
            if info_dict['shortest'] != {}:
                for n in info_dict['possibility'][info_dict['shortest']]:
                    possibility = {}
                    for ps in p:
                        possibility[ps] = p[ps]
                    possibility[info_dict['shortest']] = n
                    # possibility.update({info_dict['shortest']: n})
                    new_list.append(possibility)
                    # print(new_list)
                # print(new_list)
                info_dict['possibility'].pop(info_dict['shortest'])
        return new_list

    def solve_sdk(self, info_dict):
        info_dict = multi_sudoku.sub_points(self, info_dict)
        next_list = []
        for n in info_dict['possibility'][info_dict['shortest']]:
            next_list.append({info_dict['shortest']: n})
        # print(info_dict)
        while info_dict['possibility'] != {}:
            next_list = multi_sudoku.next_number(self, info_dict, next_list)
            # print(info_dict['possibility'])
            # print(info_dict['fixed_number'])
            if next_list == []:
                # print(info_dict)
                break
            # print(next_list)
            print(len(next_list))
        return next_list

    def show_solution(self):
        pass


if __name__ == "__main__":
    a = multi_sudoku()
    b = a.read_sdk("multi_hard_23_0.sdk")
    c = a.load_sdk_map(b)
    # print(c)
    d = a.sub_points(c)
    # print(d)
    e = a.solve_sdk(c)
    print(e)
