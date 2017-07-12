#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################


import csv
import os

f = open("TESTCSV.csv","w")

w = csv.writer(f, delimiter=";")

A = 1.226546
B = 5.1545455
C = 7.4566454

A1, A2 = str(A).split(".")
B1, B2 = str(B).split(".")
C1, C2 = str(C).split(".")

w.writerow([A1+','+A2,B1+','+B2,C1+','+C2])
f.close()