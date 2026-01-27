import numpy as np
import scipy as sp
import math 

rng = np.random.default_rng()

psi_initial = np.zeros(20,  dtype=int )

p_i = 0.5 #probability of bit flip

max_decode = math.floor((len(psi_initial)-1)/2)

for i in range(1,len(psi_initial)):
    	p = rng.random()
    	if p <= p_i and psi_initial[i] == 0:
        	psi_initial[i] = 1
    	elif p <= p_i and psi_initial[i] == 1:
        	psi_initial[i] = 0

psi_noisy = psi_initial.copy()

print("Noisy state:", psi_noisy)

#syndrome calculation

len_psi = len(psi_initial)

syndr_arr = np.zeros(len_psi - 1, dtype = int)
err_arr = [] # position of error on syndrome (1-indexing) 

for i in range(0, len_psi - 1): #0-indexing here
	if psi_initial[i] != psi_initial[i+1]: #flag domain walls with 1
		syndr_arr[i] = 1
		err_arr.append(i+1)

print("Syndrome: ", syndr_arr) 

psi_decoded = psi_noisy.copy()

trial1 = [1,1,0,0,0]
syn1 = [0,1,0,0]

def ECupdate(psi, syndromes):
	init_arr = np.zeros(2, dtype = int)
	Eloc_arr = [] #location of errors on psi 0-indexing
	Ns = len(syndromes) #note that len(syndromes) = len(psi) - 1
	Npsi = len(psi)
	for i in range(0,Ns):
		if i == 0:
			s0 = syndromes[0]
			s1 = syndromes[1]
			s2 = syndromes[2]
			if s0 != s1:
				init_arr[0] = 1
			if s0 != s2:
				init_arr[0] = 1
			if np.array_equal(init_arr, np.array([1,0])) or np.array_equal(init_arr, np.array([0,1])):
				Eloc_arr.append(1)
			if np.array_equal(init_arr, np.array([1,1])):
				Eloc_arr.append(0)
		elif i == Ns - 1:
			sN = syndromes[Ns - 1]
			sN1 = syndromes[Ns - 2]
			sN2 = syndromes[Ns - 3]
			if sN != sN1:
				init_arr[0] = 1
			if sN != sN2:
				init_arr[1] = 1
			if np.array_equal(init_arr, np.array([1,1])): #possibly rethink this one, but I think it will converge
				Eloc_arr.append(Npsi-1) #last slot on psi
			if np.array_equal(init_arr, np.array([1,0])) or np.array_equal(init_arr,np.array([0,1])):
				Eloc_arr.append(Npsi-2)
		else:
			si = syndromes[i]
			sim = syndromes[i-1]
			sip = syndromes[i+1]
			if si != sim:
				init_arr[0] = 1
			if si != sip:
				init_arr[1] = 1
			if np.array_equal(init_arr, np.array([1,0])):
				Eloc_arr.append(i+1)
			if np.array_equal(init_arr, np.array([0,1])):
				Eloc_arr.append(i)
			if np.array_equal(init_arr, np.array([1,1])):
				Eloc_arr.append(i)
		init_arr = np.zeros(2, dtype = int) #restoring init_arr
	Eloc_ammend = set(Eloc_arr)
	return Eloc_ammend

print("trial: ", ECupdate(trial1,syn1), "for noisy state:", trial1)


