import h5py
import matplotlib.pyplot as plt

from Tree_DataIO import Extract_Tree_Branches_from_HDF, Read_GT_Tree_Branches_Data

hdf5_file = "/Users/kristinaulicna/Documents/LIDo_PhD_Programme/Cells_MDCK/GV0800/pos12/HDF/segmented.hdf5"
save_trees_dr = "/Users/kristinaulicna/Documents/LIDo_PhD_Programme/Cells_MDCK/overall_analysis/publication_manuscript/PDF_Figures/"
save_gtrue_dr = "/Users/kristinaulicna/Documents/LIDo_PhD_Programme/Cells_MDCK/overall_analysis/btrack_trees_ground_truth/"


class Node(object):

    def __init__(self, ID, st=0, en=0, depth=0, left=None, right=None):
        self.ID = ID
        self.st = st
        self.en = en
        self.depth = depth
        self.left = left
        self.right = right

    @property
    def leaf(self):
        return not all([self.left, self.right])

    @property
    def children(self):
        """ return references to the children (if any) """
        if self.leaf:
            return []
        return [self.left, self.right]

    def __repr__(self):
        return f"Cell #{self.ID} -> children IDs: #{self.left} & #{self.right}"



class Lineage_Tree(object):

    def __init__(self, tree_root_ID, hdf5_file=None, txt_file=None, tree_branches_list=None):
        """ List of lists:
            - each list must have exactly 8 integer members
            - lists in ascending order according to 1st item
            - 1st list represent the root node
        """

        assert tree_branches_list is not None or hdf5_file is not None or txt_file is not None

        tree_branches = tree_branches_list
        if tree_branches_list is None:
            if hdf5_file is not None:
                tree_branches = Extract_Tree_Branches_from_HDF(tree_root_ID, hdf5_file)

            if txt_file is not None:
                tree_branches = Read_GT_Tree_Branches_Data(tree_root_ID, save_gtrue_dr)

        # Attributes:
        self.root = None
        self.tree_branches = tree_branches


    def add_child_node(self, root, branch_data):
        if root is None:
            return
        if root.ID == branch_data[3]:
            if root.left is None:
                root.left = Node(ID=branch_data[0], st=branch_data[1], en=branch_data[2], depth=branch_data[7])
                return
            if root.right is None:
                root.right = Node(ID=branch_data[0], st=branch_data[1], en=branch_data[2], depth=branch_data[7])
                return
        self.add_child_node(root.left, branch_data)
        self.add_child_node(root.right, branch_data)


    def create_tree(self):
        for enum, tree_branch in enumerate(self.tree_branches):
            if enum == 0:
                self.root = Node(ID=tree_branch[0], st=tree_branch[1], en=tree_branch[2], depth=tree_branch[7])
            else:
                self.add_child_node(root=self.root, branch_data=tree_branch)
        return self.root


    def print_tree(self):
        # recursive part:
        def _print(node, k=0):
            if node is None:
                # print('.' * k, None)
                return
            print('.' * k, node.ID)
            _print(node.left, k + 4)
            _print(node.right, k + 4)
        # non-recursive part:
        _print(self.root, 0)


    def plot_tree(self, color='black', linewidth=1.5, markersize=6, alpha=1.0, labels=False):
        plotter = LineageTreePlotter()
        plotter.plot(self.root, color, linewidth, markersize, alpha, labels)




class LineageTreePlotter_Figure(object):

    def __init__(self, axis_index, order):
        self.axis_index = axis_index
        self.order = order
        self.reset()

    def reset(self):
        self.y = 0  # reset the position iterator

    def plot(self, tree, color, linewidth, markersize, alpha, labels):

        queue, marked, y_pos = [], [], []

        # put the start vertex into the queue, and the marked list
        queue.append(tree)
        marked.append(tree)
        y_pos.append(0)

        # store the line coordinates that need to be plotted
        line_list = []
        text_list = []
        marker_list = []

        # now step through
        while len(queue) > 0:
            # pop the root from the tree
            node = queue.pop(0)
            y = y_pos.pop(0)

            # draw the root of the tree
            line_list.append(([y, y], [node.st, node.en]))
            marker_list.append((y, node.st, color, '.', linewidth, markersize, alpha))

            # TODO: Mark if this is an apoptotic tree!
            marker_list.append((y, node.en, color, 's', linewidth, markersize, alpha))
            text_list.append((y, node.en, str(node.ID), 'k'))

            if tree.ID == node.ID:
                text_list.append((y, node.st, str(node.ID), 'k'))

            for child in node.children:
                if child not in marked:

                    # mark the children
                    marked.append(child)
                    queue.append(child)

                    # calculate the depth modifier
                    depth_mod = 2. / (2. ** (node.depth - 1.))

                    if child == node.children[0]:
                        y_pos.append(y + depth_mod)
                    else:
                        y_pos.append(y - depth_mod)

                    # plot a linking line to the children
                    line_list.append(([y, y_pos[-1]], [node.en, child.st]))
                    marker_list.append((y, node.en, color, 'o', linewidth, markersize, alpha))
                    text_list.append((y_pos[-1], child.en - (child.en - child.st) / 2., str(child.ID), 'k'))

        # now that we have traversed the tree, calculate the span
        tree_span = []
        for line in line_list:
            tree_span.append(line[0][0])
            tree_span.append(line[0][1])

        min_x = min(tree_span)
        max_x = max(tree_span)

        # Plot the thing!
        y_offset = self.y - min_x + 1

        # lines
        for line in line_list:
            x, y = [xx + y_offset for xx in line[0]], line[1]
            plt.plot(x, y, '-', color=color, linewidth=linewidth, markersize=markersize, alpha=alpha)

        # markers
        for marker in marker_list:
            plt.plot(marker[0] + y_offset, marker[1], color=marker[2], marker=marker[3], linewidth=marker[4],
                     markersize=marker[5], alpha=marker[6])

        # labels
        if labels:
            label_list = []
            for txt_label in text_list:
                if txt_label[2] not in label_list:
                    label_list.append(txt_label[2])
                    plt.text(x=txt_label[0] + y_offset + 0.05, y=txt_label[1] - 0.1, s=txt_label[2], fontsize=14,
                             color=txt_label[3], rotation=45)

        # update the position for next round
        self.y = y_offset + max_x + 1



class LineageTreePlotter_Grid(object):

    def __init__(self, axis_index, order, figsize=(24, 30), nrows=8, ncols=3):
        self.axis_index = axis_index
        self.order = order
        self.figsize = figsize
        self.nrows = nrows
        self.ncols = ncols
        self.reset()

    def reset(self):
        self.y = 0  # reset the position iterator

    def plot(self, tree, color, linewidth, markersize, alpha, labels):

        fig, axs = plt.subplots(figsize=self.figsize,
                                nrows=self.nrows, ncols=self.ncols)

        queue, marked, y_pos = [], [], []

        # put the start vertex into the queue, and the marked list
        queue.append(tree)
        marked.append(tree)
        y_pos.append(0)

        # store the line coordinates that need to be plotted
        line_list = []
        text_list = []
        marker_list = []

        # now step through
        while len(queue) > 0:
            # pop the root from the tree
            node = queue.pop(0)
            y = y_pos.pop(0)

            # draw the root of the tree
            line_list.append(([y, y], [node.st, node.en]))
            marker_list.append((y, node.st, color, '.', linewidth, markersize, alpha))

            # TODO: Mark if this is an apoptotic tree!
            marker_list.append((y, node.en, color, 's', linewidth, markersize, alpha))
            text_list.append((y, node.en, str(node.ID), 'k'))

            if tree.ID == node.ID:
                text_list.append((y, node.st, str(node.ID), 'k'))

            for child in node.children:
                if child not in marked:

                    # mark the children
                    marked.append(child)
                    queue.append(child)

                    # calculate the depth modifier
                    depth_mod = 2. / (2. ** (node.depth - 1.))

                    if child == node.children[0]:
                        y_pos.append(y + depth_mod)
                    else:
                        y_pos.append(y - depth_mod)

                    # plot a linking line to the children
                    line_list.append(([y, y_pos[-1]], [node.en, child.st]))
                    marker_list.append((y, node.en, color, 'o', linewidth, markersize, alpha))
                    text_list.append((y_pos[-1], child.en - (child.en - child.st) / 2., str(child.ID), 'k'))

        # now that we have traversed the tree, calculate the span
        tree_span = []
        for line in line_list:
            tree_span.append(line[0][0])
            tree_span.append(line[0][1])

        min_x = min(tree_span)
        max_x = max(tree_span)

        # Plot the thing!
        y_offset = self.y - min_x + 1

        # lines
        for line in line_list:
            x, y = [xx + y_offset for xx in line[0]], line[1]
            axs[self.axis_index][self.order].plot(x, y, '-', color=color, linewidth=linewidth, markersize=markersize, alpha=alpha)

        # markers
        for marker in marker_list:
            axs[self.axis_index][self.order].plot(marker[0] + y_offset, marker[1], color=marker[2], marker=marker[3], linewidth=marker[4],
                     markersize=marker[5], alpha=marker[6])

        # labels
        if labels:
            for txt_label in text_list:
                axs[self.axis_index][self.order].text(x=txt_label[0] + y_offset - 0.1, y=txt_label[1] - 0.1, s=txt_label[2], fontsize=8,
                                     color=txt_label[3])

        # update the position for next round
        self.y = y_offset + max_x + 1
