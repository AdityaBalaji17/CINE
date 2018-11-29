#!C:/Users/Aditya/Anaconda2/python
import numpy as np
np.set_printoptions(threshold=np.inf)
import math
import os
def mag(x): 
    return math.sqrt(sum(i**2 for i in x))
def sigmoid(x):
  return 1 / (1 + math.exp(-x))


n_data=8
n_lines=50
n_elts=62
dataset = [[[0 for k in xrange(n_elts)] for j in xrange(n_lines)] for i in xrange(n_data)]

input_fv_file=open("fv.txt").read()
input_nos=input_fv_file.split(',')
l=1
for i in range (0,n_data):
	for j in range(0,n_lines):
		for k in range(0,n_elts):
			dataset[i][j][k]=int(input_nos[l])
			l+=1


n_output_data=8
n_output_lines=35
n_output_elts=8
outputs = [[[0 for k in xrange(n_output_elts)] for j in xrange(n_output_lines)] for i in xrange(n_output_data)]

sigmoid_outputs = [[[0 for k in xrange(n_output_elts)] for j in xrange(n_output_lines)] for i in xrange(n_output_data)]
l=1
output_fv_file=open("outputs.txt").read()
output_nos=output_fv_file.split(',')
for i in range (0,n_output_data):
	for j in range(0,n_output_lines):
		for k in range(0,n_output_elts):
			outputs[i][j][k]=int(output_nos[l])
			sigmoid_outputs[i][j][k]=sigmoid(outputs[i][j][k])
			l+=1

N0=50

#hidden layer 1
M1=N0
M2=62
M3=30

N1=45

#hidden layer 2 
M4=N1
M5=30
M6=15

N2=40

#output layer
M7=N2
M8=15
M9=8

N3=35

weights1=np.random.random((N1,M1,M2,M3))
weights2=np.random.random((N2,M4,M5,M6))
weightsOp=np.random.random((N3,M7,M8,M9))







n_neurons=N1+N2+N3


I1=np.random.random((N1,1,M3))
I2=np.random.random((N2,1,M6))
I3=np.random.random((N3,1,M9))

O1=np.random.random((N1,1,M3))
O2=np.random.random((N2,1,M6))
O3=np.random.random((N3,1,M9))


sigmoid_O1=np.random.random((N1,1,M3))
sigmoid_O2=np.random.random((N2,1,M6))
sigmoid_O3=np.random.random((N3,1,M9))


ERR1=np.random.random((N1))
ERR2=np.random.random((N2))
ERR3=np.random.random((N3))

ERR1_vector=np.random.random((N1,1,M3))
ERR2_vector=np.random.random((N2,1,M6))
ERR3_vector=np.random.random((N3,1,M9))


bias1=np.random.random((N1,1,M3))
bias2=np.random.random((N2,1,M6))
bias3=np.random.random((N3,1,M9))
for i in range(0,N1):
	for j in range(0,M3):
		bias1[i][0][j]=0.5

for i in range(0,N2):
	for j in range(0,M6):
		bias2[i][0][j]=0.5

for i in range(0,N3):
	for j in range(0,M9):
		bias3[i][0][j]=0.5

		
l_rate=0.1

for x in range(0,100):
	count=0
	for i in range(0,n_data):
		for n_i in range(0,N1):
			I1[n_i]=bias1[n_i]
		for n_i in range(0,N2):
			I2[n_i]=bias2[n_i]
		for n_i in range(0,N3):
			I3[n_i]=bias3[n_i]
		n_i=0
		for q in range(0,N1):
			for j in range(0,n_lines):
				I1[n_i]=np.add(I1[n_i],np.dot(dataset[i][j],weights1[q][j]))
				
			n_i+=1
		n_i=0
		for q in range(0,N2):
			for j in range(0,N1):
				I2[n_i]=np.add(I2[n_i],np.dot(I1[j],weights2[q][j]))
			n_i+=1
		n_i=0
		for q in range(0,N3):
			for j in range(0,N2):
				I3[n_i]=np.add(I3[n_i],np.dot(I2[j],weightsOp[q][j]))
			n_i+=1
		
		for n_i in range(0,N1):
			O1[n_i]=I1[n_i]
			for n_j in range(0,M3):
				if (O1[n_i][0][n_j]>-1000):
					sigmoid_O1[n_i][0][n_j]=sigmoid(O1[n_i][0][n_j])
				else:
					sigmoid_O1[n_i][0][n_j]=0
		for n_i in range(0,N2):
			O2[n_i]=I2[n_i]
			for n_j in range(0,M6):
				if (O2[n_i][0][n_j]>-1000):
					sigmoid_O2[n_i][0][n_j]=sigmoid(O2[n_i][0][n_j])
				else:
					sigmoid_O2[n_i][0][n_j]=0
		for n_i in range(0,N3):
			for n_j in range(0,M9):
				O3[n_i][0][n_j]=I3[n_i][0][n_j]
				if (O3[n_i][0][n_j]>-1000):
					sigmoid_O3[n_i][0][n_j]=sigmoid(O3[n_i][0][n_j])
				else:
					#print O3[n_i][0][n_j]
					sigmoid_O3[n_i][0][n_j]=0
		
		SO=np.random.random((N3,1,M9))
		for n_i in range(0,N3):
			for n_j in range(0,M9):
				SO[n_i][0][n_j]=sigmoid_outputs[i][n_i][n_j]
		ERR3_vector=np.subtract(SO,sigmoid_O3)
		
		ERR=0
		mul3=0
		for n_i in range(0,N3):
			ERR3[n_i]=0
			mul3=0
			for n_j in range(0,M9):
				mul3+=sigmoid_O3[n_i][0][n_j]*(1-sigmoid_O3[n_i][0][n_j])
				ERR3[n_i]+=abs(ERR3_vector[n_i][0][n_j])
				
			mul3/=M9
			ERR3[n_i]/=M9
			#ERR3[n_i]*=mul3
			#print ERR1[n_i]
			
		for n_i in range(0,N2):
			ERR2[n_i]=0
			for n_k in range(0,N3):
				for n_j in range(0,M8):
					for n_l in range(0,M9):
						ERR2[n_i]+=ERR3[n_k]*weightsOp[n_k][n_i][n_j][n_l]
						ERR2_vector[n_i][0][n_j]+=ERR3_vector[n_k][0][n_l]*weightsOp[n_k][n_i][n_j][n_l]
			ERR2[n_i]/=(M9*M8)
			#print ERR2[n_i]
		for n_i in range(0,N1):
			ERR1[n_i]=0
			for n_k in range(0,N2):
				for n_j in range(0,M5):
					for n_l in range(0,M6):
						ERR1[n_i]+=ERR2[n_k]*weights2[n_k][n_i][n_j][n_l]
						ERR1_vector[n_i][0][n_j]+=ERR2_vector[n_k][0][n_l]*weights2[n_k][n_i][n_j][n_l]
			ERR1[n_i]/=(M6*M5)
			#print ERR1[n_i]
		X1=np.random.random((1,M2))
		X2=np.random.random((1,M3))
		
		for n_i in range(0,N1):
			for n_j in range(0,M1):
				X1[0]=dataset[i][n_j]
				X2[0]=ERR1_vector[n_i][0]
				weights1[n_i][n_j]=np.add(weights1[n_i][n_j],np.multiply(l_rate,np.dot(np.transpose(X1),X2)))
		
		X3=np.random.random((1,M5))
		X4=np.random.random((1,M6))
		
		for n_i in range(0,N2):
			for n_j in range(0,M4):
				X3[0]=sigmoid_O1[n_j][0]
				X4[0]=ERR2_vector[n_i][0]
				weights2[n_i][n_j]=np.add(weights2[n_i][n_j],np.multiply(l_rate,np.dot(np.transpose(X3),X4)))
		
		X5=np.random.random((1,M8))
		X6=np.random.random((1,M9))
		
		for n_i in range(0,N3):
			for n_j in range(0,M7):
				X5[0]=sigmoid_O2[n_j][0]
				X6[0]=ERR3_vector[n_i][0]
				weightsOp[n_i][n_j]=np.add(weightsOp[n_i][n_j],np.multiply(l_rate,np.dot(np.transpose(X5),X6)))
		
		bias1=np.multiply(l_rate,np.add(bias1,ERR1_vector))
		bias2=np.multiply(l_rate,np.add(bias2,ERR2_vector))
		bias3=np.multiply(l_rate,np.add(bias3,ERR3_vector))
		#print sigmoid_O3
		
	print "end of epoch"+str(x)
filename="weights.txt"
string="weights1="+str(weights1)+"\nweights2="+str(weights2)+"\nweightsOp="+str(weightsOp)+"\nbias1="+str(bias1)+"\nbias2="+str(bias2)+"\nbias3="+str(bias3)+"\nbias4="
f=open(filename,"w+")
f.write(string)
print "Done"