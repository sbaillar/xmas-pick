#!/usr/bin/env python3

import numpy as np
import os
import time

class XmasPick:

    def __init__(self):
        self.categories = ["Nam", "GrB", "Exp", "Rea", "Foo", "ReG", "GiC"]
        self.picknames = ["Van", "Vin", "Val", "Dad", "Mom", "Tom", "S K"]
        self.result = np.empty((8, 7), dtype=object)
        self.count = 0
        self.badpairs = {1: "S K",
                         2: None,
                         3: "Tom",
                         4: "Mom",
                         5: "Dad",
                         6: "Val",
                         7: "Van"}
        # Cash denominations 2x 20, 6x 10, 11x 5, 23x 1

    def get_pickers(self, name):
        # print("="*30)
        # print("Picking for %s.." % name)
        pickers = self.picknames[:]
        # Cant' pick yourself
        pickers.remove(name)
        np.random.shuffle(pickers)
        # print("PICKERS = %s" % pickers)
        return pickers

    def get_row(self, xidx):
        return self.result[xidx, : ]

    def get_col(self, yidx):
        return self.result[: , yidx ]

    def get_colname(self, yidx):
        return self.result[0, yidx ]

    def setheaders(self):
        yidx = 0
        for cat in self.categories:
            self.result[0,yidx] = cat
            yidx += 1

    def setnames(self):
        xidx = 1
        for name in self.picknames:
            self.result[xidx, 0] = name
            xidx += 1

    def blank(self, x):
        for y in range(1, 7):
            self.result[x, y] = None

    def picking(self):
        self.setheaders()
        self.setnames()

        xidx = 1
        good = False
        badcount = 0
        while xidx <= 7:
            # print("x index is %s" % xidx)
            while good is False:
                try:
                    p = self.get_pickers(self.result[xidx, 0])
                    for y in range(1, 7):
                        # print("y index: %s" % y)
                        # print("PICKERS = %s" % p)
                        name = p.pop(0)
                        # print("COL = %s" % self.get_col(y))
                        if y == 5 and name == self.badpairs[xidx]:
                            # print("Bad Pair: x = %s, n = %s" % (xidx, name))
                            badcount += 1
                            raise
                        elif name not in self.get_col(y):
                            # print("placing (%s/%s)" % (name, self.get_colname(y)))
                            self.result[xidx, y] = name
                        else:
                            # print("There already is a %s in %s" % (name, self.get_colname(y)))
                            # print(self.result)
                            raise StopIteration
                    else:
                        good = True

                except StopIteration:
                    self.blank(xidx)
                    good = False

                except:
                    if badcount > 20:
                        print("Unsolvable")
                        break


            xidx += 1
            # print("Increment x index to %s" % xidx)
            good = False

        # print(self.result)
        # if badcount < 20:
        #    self.compare()
        # else:
        #    pass

    def saveresults(self):
        # print("Saving results...")
        np.savez("history/%s.npz" % int(time.time()*1000), self.result)

    def compare(self):
        unique = True
        self.count = 0
        try:
            for f in os.listdir("./history"):
                self.count += 1
                # print("Comparing file %s" % f)
                with np.load("./history/%s" % f) as B:
                    if np.array_equal(self.result, B):
                        unique = False
                        raise StopIteration

        except StopIteration:
            pass

    def printmatrix(self):
        n = 43
        print("\n"*1)
        print("="*n)
        for x in range(0,8):
           print("| %s | %s | %s | %s | %s | %s | %s |" % (self.result[x,0],
                                                           self.result[x,1],
                                                           self.result[x,2],
                                                           self.result[x,3],
                                                           self.result[x,4],
                                                           self.result[x,5],
                                                           self.result[x,6] ))
        print("="*n)
        print("\n"*1)
        #print("\n\nFound %s unique solutions" % self.count)


if __name__ == '__main__':
    runs = 25
    os.system('clear')
    while runs >= 1:
        print("RUN: %s" % runs)
        x = XmasPick()
        x.picking()
        if runs == 1:
            os.system('clear')
            x.printmatrix()
        runs -= 1
