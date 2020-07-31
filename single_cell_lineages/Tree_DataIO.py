import os
import h5py


hdf5_file = "/Users/kristinaulicna/Documents/LIDo_PhD_Programme/Cells_MDCK/GV0800/pos12/HDF/segmented.hdf5"
save_trees_dr = "/Users/kristinaulicna/Documents/LIDo_PhD_Programme/Cells_MDCK/overall_analysis/publication_manuscript/PDF_Figures/"
save_gtrue_dr = "/Users/kristinaulicna/Documents/LIDo_PhD_Programme/Cells_MDCK/overall_analysis/btrack_trees_ground_truth/"


def Extract_Tree_Branches_from_HDF(tree_root_ID, hdf5_file):
    tree_branches = []

    with h5py.File(hdf5_file, 'r') as f:
        for cell, progeny in zip(f['tracks']['obj_type_1']['LBEPR'], f['tracks']['obj_type_1']['Ch_Ch_Gen_CCT']):
            if int(cell[0]) == tree_root_ID or int(cell[4]) == tree_root_ID:
                tree_branches.append([int(i) for i in cell] + [int(i) for i in progeny[:-1]])

    return sorted(tree_branches)


def Read_GT_Tree_Branches_Data(tree_root_ID, save_gtrue_dr):
    tree_branches = []
    file = save_gtrue_dr + f"LinTree_Root_{tree_root_ID}_Ground_Truth.txt"

    if not os.path.isfile(file):
        file = save_gtrue_dr + f"LinTree_Root_{tree_root_ID}.txt"

    if not os.path.isfile(file):
        print (f"File with Tree #{tree_root_ID} doesn't exist")

    else:
        with open(file, "r") as txt_file:
            for line in txt_file:
                line = [int(i) for i in line.rstrip().split('\t')]

                assert len(line) == 8
                tree_branches.append(line)

    #return sorted(tree_branches)
    return tree_branches


def Write_GT_Tree_Branches_Data(tree_root_ID, tree_branches_gt, save_gt_dr):
    file = save_gt_dr + f"LinTree_Root_{tree_root_ID}_Ground_Truth.txt"
    #file = save_gt_dr + f"LinTree_Root_{tree_root_ID}.txt"

    if not os.path.isfile(file):
        file = save_gt_dr + f"LinTree_Root_{tree_root_ID}.txt"

    with open(file, "w") as txt_file:
        string = ''
        #for branch in sorted(tree_branches_gt):
        for branch in tree_branches_gt:
            for item in branch:
                string += str(item) + "\t"
            string = string[:-1] + "\n"
        txt_file.write(string)

    print (f"Done for Tree #{tree_root_ID}")


#tree_branches = Read_GT_Tree_Branches_Data(tree_root_ID=38, save_gtrue_dr=save_gtrue_dr)
#print (tree_branches)