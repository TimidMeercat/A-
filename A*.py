import numpy as np
import bisect


class Node:
    def __init__(self, data, level, fval):
        """Initialize Node with data, level and calculated f value"""
        self.data = np.array(data)
        self.level = level
        # f = level + h-value
        self.fval = fval
        self.predecessor = None
        self.zp = np.where(self.data == '0')
        self.op = None

        # comparison method
    def __lt__(self, other):
        return self.fval < other.fval

        # representation/print method
    def __repr__(self):
        return self.data

    # methods to move blank tile
    def move_up(self):
        if self.zp[0] > 0:
            n1 = np.copy(self.data)
            pos = np.copy(self.zp)
            pos[0] -= 1
            n1[tuple(self.zp)] = n1[tuple(pos)]
            n1[tuple(pos)] = '0'
            return n1
        return None

    def move_left(self):
        if self.zp[1] > 0:
            n2 = np.copy(self.data)
            pos = np.copy(self.zp)
            pos[1] -= 1
            n2[tuple(self.zp)] = n2[tuple(pos)]
            n2[tuple(pos)] = '0'
            return n2
        return None

    def move_right(self):
        if self.zp[1] < 2:
            n3 = np.copy(self.data)
            pos = np.copy(self.zp)
            pos[1] += 1
            n3[tuple(self.zp)] = n3[tuple(pos)]
            n3[tuple(pos)] = '0'
            return n3
        return None

    def move_down(self):
        if self.zp[0] < 2:
            n4 = np.copy(self.data)
            pos = np.copy(self.zp)
            pos[0] += 1
            n4[tuple(self.zp)] = n4[tuple(pos)]
            n4[tuple(pos)] = '0'
            return n4
        return None

    # method to generate successors nodes
    def successors(self):
        childNodes = []
        n1 = self.move_up()
        n2 = self.move_down()
        n3 = self.move_left()
        n4 = self.move_right()

        if n1 is not None and self.op != 'D':
            n1 = Node(n1, self.level + 1, 0)
            n1.op = 'U'
            childNodes += n1,
        if n2 is not None and self.op != 'U':
            n2 = Node(n2, self.level + 1, 0)
            n2.op = 'D'
            childNodes += n2,
        if n3 is not None and self.op != 'R':
            n3 = Node(n3, self.level + 1, 0)
            n3.op = 'L'
            childNodes += n3,
        if n4 is not None and self.op != 'L':
            n4 = Node(n4, self.level + 1, 0)
            n4.op = 'R'
            childNodes += n4,
        return childNodes


class Solve:
    def __init__(self):
        self.size = 3
        self.open = []
        self.closed = []
        self.goal = np.array([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']])

    def take_input(self):
        tnode = []
        print("Enter the numbers row wise with 0 as blank position\n")
        for i in range(self.size):
            temp = input().split()
            tnode += [temp]
        for i in tnode:
            if len(i) != 3:
                print('Invalid Input')
                exit()
        if len(tnode) == 3:
            return tnode
        else:
            print('Invalid Input')
            exit()

    def fvalue(self, node, goal):

        return self.hvalue(node.data, goal) + node.level

    # Calculates the number of squares that are not in the right place
    def hvalue(self, nodeData, goalData):
        temp = 0
        for i in range(self.size):
            for j in range(self.size):
                if nodeData[i][j] != goalData[i][j] and nodeData[i][j] != '0':
                    temp += 1
        return temp

    def f2value(self, node, goal):

        return self.h2value(node.data, goal) + node.level

    # Calculates the manhattan distance
    def h2value(self, nodeData, goalData):
        val = 0
        for x, y in np.ndindex(nodeData.shape):
            temp = nodeData[x, y]
            if temp != '0':
                pos2 = np.where(goalData == temp)
                val += (abs(pos2[0] - x) + abs(pos2[1] - y))
        return val[0]

    # Checks if the input state is solvable
    def solvability(self, rootNode):
        try:
            checkNode = np.concatenate(rootNode, axis=0)
            checkNode = np.array(list(map(int, checkNode)))
            checkNode = checkNode[checkNode != 0]
            mask = checkNode > 8
            if True in mask:
                raise Exception
            chngs = 0
            for i in range(len(checkNode) - 1):
                b = np.array(np.where(checkNode[i + 1:] < checkNode[i])).reshape(-1)
                chngs += len(b)
            return chngs
        except:
            print('Invalid Input')
            exit()

    # After finding solution ...
    def showPath(self):
        path = [self.open[0]]
        op = [self.open[0].op]
        while path[-1].predecessor.predecessor is not None:
            path += path[-1].predecessor,
            op += path[-1].op,
        path += self.closed[0],
        del path[0]
        path.reverse()
        op.reverse()
        for i in path:
            for j in i.data:
                print(j)
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
        for i in self.open[0].data:
            print(i)
        print('\nOptimal Path:')
        print(op)
        exit()

    # sorts and inserts the new nodes as per the fvalue
    def insert(self, newNode):
        newNode.fval = self.f2value(newNode, self.goal)
        bisect.insort(self.open, newNode)
        return

    def start(self):
        rootNode = self.take_input()
        if self.solvability(rootNode) % 2 == 0:
            rootNode = Node(rootNode, 0, 0)
            self.open += rootNode,
            while 1:
                if self.open is None:
                    print('No Solution')
                    exit()
                curNode = self.open[0]
                del self.open[0]
                self.closed += curNode,
                # print(f'Total nodes explored are {len(self.open) + len(self.closed)}')
                if (curNode.fval - curNode.level) == 0 and curNode.level != 0:
                    print(f'Solution Found at level {curNode.level}')
                    self.showPath()

                for i in curNode.successors():
                    i.predecessor = curNode
                    self.insert(i)
        else:
            print('No solution for given input')
            exit()

s = Solve()
s.start()
