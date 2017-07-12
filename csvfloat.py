#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

# Allow us to define float that are read by Excel in the CSV file : 245,454545
# The coma is very important (maybe due to my French version of Excel, I need to check this)
def csvfloat(n, d=6):
	A = str(round(n,d)).split(".")
	if len(A) == 2:
		return A[0]+','+A[1]
	else:
		B = str(round(n,d)).split("e")
		if int(B[1])>0:
			return B[0]+abs(int(B[1]))*str(0)+','+str(0)
		else:
			return str(0)+','+(abs(int(B[1]))-1)*str(0)+B[0]
	