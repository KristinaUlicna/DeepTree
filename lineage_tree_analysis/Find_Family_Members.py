# Write a script to look for family members...

import h5py


class Find_Family(object):
    """
    def __init__(self, hdf5_file, cell_ID):

        # Check if cell_ID is an integer:
        assert isinstance(cell_ID, int)
        self.cell_ID = cell_ID

        self.cells_all = []
        self.cells_real = []

        # Make a record of non-root, non-leaf cells:
        with h5py.File(hdf5_file, 'r') as f:

            self.lbepr_1 = list(f['tracks']['obj_type_1']['LBEPR'])
            self.lbepr_2 = list(f['tracks']['obj_type_1']['Ch_Ch_Gen_CCT'])

            for cell, progeny in zip(self.lbepr_1, self.lbepr_2):
                self.cells_all.append(cell[0])
                if cell[4] != 0 and progeny[0] != 0 and progeny[1] != 0:
                    self.cells_real.append(cell[0])
    """

    def __init__(self, lbepr_1, lbepr_2, cells_all, cells_real, cell_ID):

        # Check if cell_ID is an integer:
        self.lbepr_1 = lbepr_1
        self.lbepr_2 = lbepr_2
        self.cells_all = cells_all
        self.cells_real = cells_real
        self.cell_ID = cell_ID


    def Find_Itself(self):

        if self.cell_ID not in self.cells_all:
            return [None, None, None]

        itself_idx = self.cells_all.index(self.cell_ID)
        itself_gen = int(self.lbepr_2[itself_idx][2])
        itself_cct = float(self.lbepr_2[itself_idx][3])

        if self.cell_ID not in self.cells_real:
            itself_cct = None

        return [self.cell_ID, itself_gen, itself_cct]


    def Find_Mother(self):
        data_itself = self.Find_Itself()
        if data_itself == [None, None, None]:
            return [None, None, None]

        itself_idx = self.cells_all.index(data_itself[0])
        mother_ID = self.lbepr_1[itself_idx][3]
        if mother_ID == 0:
            return [None, None, None]

        mother_idx = self.cells_all.index(mother_ID)
        mother_gen = int(self.lbepr_2[mother_idx][2])
        mother_cct = float(self.lbepr_2[mother_idx][3])

        if mother_ID not in self.cells_real:
            mother_cct = None

        return [mother_ID, mother_gen, mother_cct]


    def Find_Sister(self):
        data_itself = self.Find_Itself()
        if data_itself == [None, None, None]:
            return [None, None, None]

        data_mother = self.Find_Mother()
        if data_mother == [None, None, None]:
            return [None, None, None]

        mother_idx = self.cells_all.index(data_mother[0])
        children = [int(self.lbepr_2[mother_idx][0]), int(self.lbepr_2[mother_idx][1])]
        sister_ID = [item for item in children if item != data_itself[0]][0]

        sister_idx = self.cells_all.index(sister_ID)
        sister_gen = int(self.lbepr_2[sister_idx][2])
        sister_cct = float(self.lbepr_2[sister_idx][3])

        if sister_ID not in self.cells_real:
            sister_cct = None

        return [sister_ID, sister_gen, sister_cct]


    def Find_Grandmother(self):
        data_mother = self.Find_Mother()
        if data_mother == [None, None, None]:
            return [None, None, None]

        mother_idx = self.cells_all.index(data_mother[0])
        grandmother_ID = self.lbepr_1[mother_idx][3]
        if grandmother_ID == 0:
            return [None, None, None]

        grandmother_idx = self.cells_all.index(grandmother_ID)
        grandmother_gen = int(self.lbepr_2[grandmother_idx][2])
        grandmother_cct = float(self.lbepr_2[grandmother_idx][3])

        if grandmother_ID not in self.cells_real:
            grandmother_cct = None

        return [grandmother_ID, grandmother_gen, grandmother_cct]


    def Find_Aunt(self):
        data_grandmother = self.Find_Grandmother()
        if data_grandmother == [None, None, None]:
            return [None, None, None]

        data_mother = self.Find_Mother()
        if data_mother == [None, None, None]:
            return [None, None, None]

        grandmother_idx = self.cells_all.index(data_grandmother[0])
        grandma_children = [int(self.lbepr_2[grandmother_idx][0]), int(self.lbepr_2[grandmother_idx][1])]
        aunt_ID = [item for item in grandma_children if item != data_mother[0]][0]

        aunt_idx = self.cells_all.index(aunt_ID)
        aunt_gen = int(self.lbepr_2[aunt_idx][2])
        aunt_cct = float(self.lbepr_2[aunt_idx][3])

        if aunt_ID not in self.cells_real:
            aunt_cct = None

        return [aunt_ID, aunt_gen, aunt_cct]


    def Find_FirstCousins(self):
        """ :return: a tuple of 2 lists instead of just 1: there are 2 cousins in a full tree."""

        data_aunt = self.Find_Aunt()
        if data_aunt == [None, None, None]:
            return ([None, None, None], [None, None, None])

        if data_aunt[2] is None:
            return ([None, None, None], [None, None, None])

        aunt_idx = self.cells_all.index(data_aunt[0])
        cousins_ID_list = [int(self.lbepr_2[aunt_idx][0]), int(self.lbepr_2[aunt_idx][1])]

        cousins = [[None, None, None], [None, None, None]]

        for enum, cousin_ID in enumerate(cousins_ID_list):
            cousins[enum][0] = cousin_ID

            cousin_idx = self.cells_all.index(cousin_ID)
            cousins[enum][1] = int(self.lbepr_2[cousin_idx][2])

            if cousin_ID in self.cells_real:
                cousins[enum][2] = float(self.lbepr_2[cousin_idx][3])

        return (cousins[0], cousins[1])


    def Find_Greatgrandmother(self):
        data_grandmother = self.Find_Grandmother()
        if data_grandmother == [None, None, None]:
            return [None, None, None]

        grandmother_idx = self.cells_all.index(data_grandmother[0])
        greatgrandmother_ID = self.lbepr_1[grandmother_idx][3]
        if greatgrandmother_ID == 0:
            return [None, None, None]

        greatgrandmother_idx = self.cells_all.index(greatgrandmother_ID)
        greatgrandmother_gen = int(self.lbepr_2[greatgrandmother_idx][2])
        greatgrandmother_cct = float(self.lbepr_2[greatgrandmother_idx][3])

        if greatgrandmother_ID not in self.cells_real:
            greatgrandmother_cct = None

        return [greatgrandmother_ID, greatgrandmother_gen, greatgrandmother_cct]


    def Find_Greataunt(self):
        data_greatgrandmother = self.Find_Greatgrandmother()
        if data_greatgrandmother == [None, None, None]:
            return [None, None, None]

        data_grandmother = self.Find_Grandmother()
        if data_grandmother == [None, None, None]:
            return [None, None, None]

        greatgrandmother_idx = self.cells_all.index(data_greatgrandmother[0])
        greatgrandma_children = [int(self.lbepr_2[greatgrandmother_idx][0]), int(self.lbepr_2[greatgrandmother_idx][1])]
        greataunt_ID = [item for item in greatgrandma_children if item != data_grandmother[0]][0]

        greataunt_idx = self.cells_all.index(greataunt_ID)
        greataunt_gen = int(self.lbepr_2[greataunt_idx][2])
        greataunt_cct = float(self.lbepr_2[greataunt_idx][3])

        if greataunt_ID not in self.cells_real:
            greataunt_cct = None

        return [greataunt_ID, greataunt_gen, greataunt_cct]


    def Find_FirstCousinsOnceRemoved(self):
        """ :return: a tuple of 2 lists instead of just 1: there are 2 cousins once removed in a full tree."""

        data_greataunt = self.Find_Greataunt()
        if data_greataunt == [None, None, None]:
            return ([None, None, None], [None, None, None])

        if data_greataunt[2] is None:
            return ([None, None, None], [None, None, None])

        greataunt_idx = self.cells_all.index(data_greataunt[0])
        cousrem_ID_list = [int(self.lbepr_2[greataunt_idx][0]), int(self.lbepr_2[greataunt_idx][1])]

        cousrems = ([None, None, None], [None, None, None])

        for enum, cousrem_ID in enumerate(cousrem_ID_list):
            cousrems[enum][0] = cousrem_ID

            cousrem_idx = self.cells_all.index(cousrem_ID)
            cousrems[enum][1] = int(self.lbepr_2[cousrem_idx][2])

            if cousrem_ID in self.cells_real:
                cousrems[enum][2] = float(self.lbepr_2[cousrem_idx][3])

        return cousrems


    def Find_SecondCousins(self):
        """ Change the structure of the code compared to others functions:
            :return: a tuple of 4 lists instead of just 1:
                     there are 4 second cousins in a full tree."""

        second_cousins = ([None, None, None], [None, None, None], [None, None, None], [None, None, None])

        data_cousrems = self.Find_FirstCousinsOnceRemoved()
        if data_cousrems == ([None, None, None], [None, None, None]):
            return second_cousins

        for e, data_cousrem in enumerate(data_cousrems):
            if data_cousrem[2] is None:
                continue

            cousrem_idx = self.cells_all.index(data_cousrem[0])
            second_cousins_ID_list = [int(self.lbepr_2[cousrem_idx][0]), int(self.lbepr_2[cousrem_idx][1])]

            for enum, second_cousin_ID in enumerate(second_cousins_ID_list):
                index = e * 2 + enum
                second_cousins[index][0] = second_cousin_ID

                second_cousin_idx = self.cells_all.index(second_cousin_ID)
                second_cousins[index][1] = int(self.lbepr_2[second_cousin_idx][2])

                if second_cousin_ID in self.cells_real:
                    second_cousins[index][2] = float(self.lbepr_2[second_cousin_idx][3])

        return second_cousins


    def Find_Greatgreatgrandmother(self):
        data_greatgrandmother = self.Find_Greatgrandmother()
        if data_greatgrandmother == [None, None, None]:
            return [None, None, None]

        greatgrandmother_idx = self.cells_all.index(data_greatgrandmother[0])
        greatgreatgrandmother_ID = self.lbepr_1[greatgrandmother_idx][3]
        if greatgreatgrandmother_ID == 0:
            return [None, None, None]

        greatgreatgrandmother_idx = self.cells_all.index(greatgreatgrandmother_ID)
        greatgreatgrandmother_gen = int(self.lbepr_2[greatgreatgrandmother_idx][2])
        greatgreatgrandmother_cct = float(self.lbepr_2[greatgreatgrandmother_idx][3])

        if greatgreatgrandmother_ID not in self.cells_real:
            greatgreatgrandmother_cct = None

        return [greatgreatgrandmother_ID, greatgreatgrandmother_gen, greatgreatgrandmother_cct]


    def Find_Greatgrandaunt(self):
        data_greatgreatgrandmother = self.Find_Greatgreatgrandmother()
        if data_greatgreatgrandmother == [None, None, None]:
            return [None, None, None]

        data_greatgrandmother = self.Find_Greatgrandmother()
        if data_greatgrandmother == [None, None, None]:
            return [None, None, None]

        greatgreatgrandmother_idx = self.cells_all.index(data_greatgreatgrandmother[0])
        greatgreatgrandma_children = [int(self.lbepr_2[greatgreatgrandmother_idx][0]), int(self.lbepr_2[greatgreatgrandmother_idx][1])]
        greatgreataunt_ID = [item for item in greatgreatgrandma_children if item != data_greatgrandmother[0]][0]

        greatgreataunt_idx = self.cells_all.index(greatgreataunt_ID)
        greatgreataunt_gen = int(self.lbepr_2[greatgreataunt_idx][2])
        greatgreataunt_cct = float(self.lbepr_2[greatgreataunt_idx][3])

        if greatgreataunt_ID not in self.cells_real:
            greatgreataunt_cct = None

        return [greatgreataunt_ID, greatgreataunt_gen, greatgreataunt_cct]


    def Find_FirstCousinsTwiceRemoved(self):
        """ :return: a tuple of 2 lists instead of just 1: there are 2 cousins once removed in a full tree."""

        data_greatgreataunt = self.Find_Greatgrandaunt()
        if data_greatgreataunt == [None, None, None]:
            return ([None, None, None], [None, None, None])

        if data_greatgreataunt[2] is None:
            return ([None, None, None], [None, None, None])

        greatgreataunt_idx = self.cells_all.index(data_greatgreataunt[0])
        coustwicerem_ID_list = [int(self.lbepr_2[greatgreataunt_idx][0]), int(self.lbepr_2[greatgreataunt_idx][1])]

        coustwicerem = ([None, None, None], [None, None, None])

        for enum, coustwicerem_ID in enumerate(coustwicerem_ID_list):
            coustwicerem[enum][0] = coustwicerem_ID

            coustwicerem_idx = self.cells_all.index(coustwicerem_ID)
            coustwicerem[enum][1] = int(self.lbepr_2[coustwicerem_idx][2])

            if coustwicerem_ID in self.cells_real:
                coustwicerem[enum][2] = float(self.lbepr_2[coustwicerem_idx][3])

        return coustwicerem


    def Find_SecondCousinsOnceRemoved(self):
        """ Change the structure of the code compared to others functions:
            :return: a tuple of 4 lists instead of just 1:
                     there are 4 second cousins in a full tree."""

        second_cousins_once_rem = ([None, None, None], [None, None, None], [None, None, None], [None, None, None])

        data_coustwicerems = self.Find_FirstCousinsTwiceRemoved()
        if data_coustwicerems == ([None, None, None], [None, None, None]):
            return second_cousins_once_rem

        for e, data_coustwicerem in enumerate(data_coustwicerems):
            if data_coustwicerem[2] is None:
                continue

            coustwicerem_idx = self.cells_all.index(data_coustwicerem[0])
            second_cousins_once_rem_ID_list = [int(self.lbepr_2[coustwicerem_idx][0]), int(self.lbepr_2[coustwicerem_idx][1])]

            for enum, second_cousin_once_rem_ID in enumerate(second_cousins_once_rem_ID_list):
                index = e * 2 + enum
                second_cousins_once_rem[index][0] = second_cousin_once_rem_ID

                second_cousin_once_rem_idx = self.cells_all.index(second_cousin_once_rem_ID)
                second_cousins_once_rem[index][1] = int(self.lbepr_2[second_cousin_once_rem_idx][2])

                if second_cousin_once_rem_ID in self.cells_real:
                    second_cousins_once_rem[index][2] = float(self.lbepr_2[second_cousin_once_rem_idx][3])

        return second_cousins_once_rem


    def Find_ThirdCousins(self):
        """ Change the structure of the code compared to others functions:
            :return: a tuple of 8 lists instead of just 1:
                     there are 8 second cousins in a full tree."""

        third_cousins = ([None, None, None], [None, None, None], [None, None, None], [None, None, None],
                         [None, None, None], [None, None, None], [None, None, None], [None, None, None])

        data_cousoncerems = self.Find_SecondCousinsOnceRemoved()
        if data_cousoncerems == ([None, None, None], [None, None, None], [None, None, None], [None, None, None]):
            return third_cousins

        for e, data_cousoncerems in enumerate(data_cousoncerems):
            if data_cousoncerems[2] is None:
                continue

            secondcousoncerem_idx = self.cells_all.index(data_cousoncerems[0])
            third_cousins_ID_list = [int(self.lbepr_2[secondcousoncerem_idx][0]),
                                     int(self.lbepr_2[secondcousoncerem_idx][1])]

            for enum, third_cousins_ID in enumerate(third_cousins_ID_list):
                index = e * 2 + enum
                third_cousins[index][0] = third_cousins_ID

                third_cousins_idx = self.cells_all.index(third_cousins_ID)
                third_cousins[index][1] = int(self.lbepr_2[third_cousins_idx][2])

                if third_cousins_ID in self.cells_real:
                    third_cousins[index][2] = float(self.lbepr_2[third_cousins_idx][3])

        return third_cousins


    def Find_Greatgreatgreatgrandmother(self):
        data_greatgreatgrandmother = self.Find_Greatgreatgrandmother()
        if data_greatgreatgrandmother == [None, None, None]:
            return [None, None, None]

        greatgreatgrandmother_idx = self.cells_all.index(data_greatgreatgrandmother[0])
        greatgreatgreatgrandmother_ID = self.lbepr_1[greatgreatgrandmother_idx][3]
        if greatgreatgreatgrandmother_ID == 0:
            return [None, None, None]

        greatgreatgreatgrandmother_idx = self.cells_all.index(greatgreatgreatgrandmother_ID)
        greatgreatgreatgrandmother_gen = int(self.lbepr_2[greatgreatgreatgrandmother_idx][2])
        greatgreatgreatgrandmother_cct = float(self.lbepr_2[greatgreatgreatgrandmother_idx][3])

        if greatgreatgreatgrandmother_ID not in self.cells_real:
            greatgreatgreatgrandmother_cct = None

        return [greatgreatgreatgrandmother_ID, greatgreatgreatgrandmother_gen, greatgreatgreatgrandmother_cct]


    def Find_Greatgreatgrandaunt(self):
        data_greatgreatgrandmother = self.Find_Greatgreatgreatgrandmother()
        if data_greatgreatgrandmother == [None, None, None]:
            return [None, None, None]

        data_greatgrandmother = self.Find_Greatgrandmother()
        if data_greatgrandmother == [None, None, None]:
            return [None, None, None]

        greatgreatgrandmother_idx = self.cells_all.index(data_greatgreatgrandmother[0])
        greatgreatgrandma_children = [int(self.lbepr_2[greatgreatgrandmother_idx][0]), int(self.lbepr_2[greatgreatgrandmother_idx][1])]
        greatgreataunt_ID = [item for item in greatgreatgrandma_children if item != data_greatgrandmother[0]][0]

        greatgreataunt_idx = self.cells_all.index(greatgreataunt_ID)
        greatgreataunt_gen = int(self.lbepr_2[greatgreataunt_idx][2])
        greatgreataunt_cct = float(self.lbepr_2[greatgreataunt_idx][3])

        if greatgreataunt_ID not in self.cells_real:
            greatgreataunt_cct = None

        return [greatgreataunt_ID, greatgreataunt_gen, greatgreataunt_cct]


    def Find_FirstCousinsThriceRemoved(self):
        """ :return: a tuple of 2 lists instead of just 1: there are 2 cousins once removed in a full tree."""

        data_greatgreataunt = self.Find_Greatgreatgrandaunt()
        if data_greatgreataunt == [None, None, None]:
            return ([None, None, None], [None, None, None])

        if data_greatgreataunt[2] is None:
            return ([None, None, None], [None, None, None])

        greatgreataunt_idx = self.cells_all.index(data_greatgreataunt[0])
        coustwicerem_ID_list = [int(self.lbepr_2[greatgreataunt_idx][0]), int(self.lbepr_2[greatgreataunt_idx][1])]

        coustwicerem = ([None, None, None], [None, None, None])

        for enum, coustwicerem_ID in enumerate(coustwicerem_ID_list):
            coustwicerem[enum][0] = coustwicerem_ID

            coustwicerem_idx = self.cells_all.index(coustwicerem_ID)
            coustwicerem[enum][1] = int(self.lbepr_2[coustwicerem_idx][2])

            if coustwicerem_ID in self.cells_real:
                coustwicerem[enum][2] = float(self.lbepr_2[coustwicerem_idx][3])

        return coustwicerem


    def Find_SecondCousinsTwiceRemoved(self):
        """ Change the structure of the code compared to others functions:
            :return: a tuple of 4 lists instead of just 1:
                     there are 4 second cousins in a full tree."""

        second_cousins_once_rem = ([None, None, None], [None, None, None], [None, None, None], [None, None, None])

        data_coustwicerems = self.Find_FirstCousinsThriceRemoved()
        if data_coustwicerems == ([None, None, None], [None, None, None]):
            return second_cousins_once_rem

        for e, data_coustwicerem in enumerate(data_coustwicerems):
            if data_coustwicerem[2] is None:
                continue

            coustwicerem_idx = self.cells_all.index(data_coustwicerem[0])
            second_cousins_once_rem_ID_list = [int(self.lbepr_2[coustwicerem_idx][0]), int(self.lbepr_2[coustwicerem_idx][1])]

            for enum, second_cousin_once_rem_ID in enumerate(second_cousins_once_rem_ID_list):
                index = e * 2 + enum
                second_cousins_once_rem[index][0] = second_cousin_once_rem_ID

                second_cousin_once_rem_idx = self.cells_all.index(second_cousin_once_rem_ID)
                second_cousins_once_rem[index][1] = int(self.lbepr_2[second_cousin_once_rem_idx][2])

                if second_cousin_once_rem_ID in self.cells_real:
                    second_cousins_once_rem[index][2] = float(self.lbepr_2[second_cousin_once_rem_idx][3])

        return second_cousins_once_rem


    def Find_ThirdCousinsOnceRemoved(self):
        """ Change the structure of the code compared to others functions:
            :return: a tuple of 8 lists instead of just 1:
                     there are 8 second cousins in a full tree."""

        third_cousins = ([None, None, None], [None, None, None], [None, None, None], [None, None, None],
                         [None, None, None], [None, None, None], [None, None, None], [None, None, None])

        data_cousoncerems = self.Find_SecondCousinsTwiceRemoved()
        if data_cousoncerems == ([None, None, None], [None, None, None], [None, None, None], [None, None, None]):
            return third_cousins

        for e, data_cousoncerems in enumerate(data_cousoncerems):
            if data_cousoncerems[2] is None:
                continue

            secondcousoncerem_idx = self.cells_all.index(data_cousoncerems[0])
            third_cousins_ID_list = [int(self.lbepr_2[secondcousoncerem_idx][0]),
                                     int(self.lbepr_2[secondcousoncerem_idx][1])]

            for enum, third_cousins_ID in enumerate(third_cousins_ID_list):
                index = e * 2 + enum
                third_cousins[index][0] = third_cousins_ID

                third_cousins_idx = self.cells_all.index(third_cousins_ID)
                third_cousins[index][1] = int(self.lbepr_2[third_cousins_idx][2])

                if third_cousins_ID in self.cells_real:
                    third_cousins[index][2] = float(self.lbepr_2[third_cousins_idx][3])

        return third_cousins


    def Find_FourthCousins(self):
        """ Change the structure of the code compared to others functions:
            :return: a tuple of 16 lists instead of just 1:
                     there are 16 second cousins in a full tree."""

        third_cousins = ([None, None, None], [None, None, None], [None, None, None], [None, None, None],
                         [None, None, None], [None, None, None], [None, None, None], [None, None, None],
                         [None, None, None], [None, None, None], [None, None, None], [None, None, None],
                         [None, None, None], [None, None, None], [None, None, None], [None, None, None])

        data_cousoncerems = self.Find_ThirdCousinsOnceRemoved()
        if data_cousoncerems == ([None, None, None], [None, None, None], [None, None, None], [None, None, None],
                                 [None, None, None], [None, None, None], [None, None, None], [None, None, None]):
            return third_cousins

        for e, data_cousoncerems in enumerate(data_cousoncerems):
            if data_cousoncerems[2] is None:
                continue

            secondcousoncerem_idx = self.cells_all.index(data_cousoncerems[0])
            third_cousins_ID_list = [int(self.lbepr_2[secondcousoncerem_idx][0]),
                                     int(self.lbepr_2[secondcousoncerem_idx][1])]

            for enum, third_cousins_ID in enumerate(third_cousins_ID_list):
                index = e * 2 + enum
                third_cousins[index][0] = third_cousins_ID

                third_cousins_idx = self.cells_all.index(third_cousins_ID)
                third_cousins[index][1] = int(self.lbepr_2[third_cousins_idx][2])

                if third_cousins_ID in self.cells_real:
                    third_cousins[index][2] = float(self.lbepr_2[third_cousins_idx][3])

        return third_cousins


    def Find_Greatgreatgreatgreatgrandmother(self):
        """ This function will yield only 2 pairs of cells in the CCT ranged <7, 42> MDCK dataset. """

        data_greatgreatgrandmother = self.Find_Greatgreatgreatgrandmother()
        if data_greatgreatgrandmother == [None, None, None]:
            return [None, None, None]

        greatgreatgrandmother_idx = self.cells_all.index(data_greatgreatgrandmother[0])
        greatgreatgreatgrandmother_ID = self.lbepr_1[greatgreatgrandmother_idx][3]
        if greatgreatgreatgrandmother_ID == 0:
            return [None, None, None]

        greatgreatgreatgrandmother_idx = self.cells_all.index(greatgreatgreatgrandmother_ID)
        greatgreatgreatgrandmother_gen = int(self.lbepr_2[greatgreatgreatgrandmother_idx][2])
        greatgreatgreatgrandmother_cct = float(self.lbepr_2[greatgreatgreatgrandmother_idx][3])

        if greatgreatgreatgrandmother_ID not in self.cells_real:
            greatgreatgreatgrandmother_cct = None

        return [greatgreatgreatgrandmother_ID, greatgreatgreatgrandmother_gen, greatgreatgreatgrandmother_cct]



# TODO: Do logical checks in terms of generational depths!

"""
# Call the class:
hdf5_file = "/Users/kristinaulicna/Documents/LIDo_PhD_Programme/Cells_MDCK/GV0800/pos12/HDF/segmented.hdf5"
call = Find_Family(hdf5_file=hdf5_file, cell_ID=1155)
itself = call.Find_Itself()
print (f"Itself = {itself}")
mother = call.Find_Mother()
print (f"Mother = {mother}")
sister = call.Find_Sister()
print (f"Sister = {sister}")
grandmother = call.Find_Grandmother()
print (f"Grandmother = {grandmother}")
aunt = call.Find_Aunt()
print (f"Aunt = {aunt}")
cousins = call.Find_Cousins()
print (f"Cousins = {cousins}")
greatgrandmother = call.Find_Greatgrandmother()
print (f"Greatgrandmother = {greatgrandmother}")
greataunt = call.Find_Greataunt()
print (f"Greataunt = {greataunt}")
cousins_once_removed = call.Find_CousinsOnceRemoved()
print (f"Cousins once removed = {cousins_once_removed}")
second_cousins = call.Find_SecondCousins()
print (f"Second Cousins = {second_cousins}")
"""