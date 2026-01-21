import numpy as np
import scipy as sp
import math 

rng = np.random.default_rng()

psi_initial = np.zeros(10,  dtype=int )
 
p_arr = np.linspace(0.0001,0.8,20) #probability of bit flip
success_arr = []

max_decode = math.floor((len(psi_initial)-1)/2)

Nits = 10000

# the amound of loops is criminal, should rewrite this code using functions :(
for p_i in p_arr: 
	for n in range(Nits):
		for i in range(1,len(psi_initial)):
    			p = rng.random()
    			if p <= p_i and psi_initial[i] == 0:
        			psi_initial[i] = 1
    			elif p <= p_i and psi_initial[i] == 1:
        			psi_initial[i] = 0

		psi_noisy = psi_initial.copy()

		#print("Noisy state:", psi_noisy)

		#syndrome calculation

		len_psi = len(psi_initial)

		syndr_arr = np.zeros(len_psi - 1, dtype = int)
		err_arr = [] # position of error on syndrome (1-indexing) 

		for i in range(0, len_psi - 1): #0-indexing here
			if psi_initial[i] != psi_initial[i+1]: #flag domain walls with 1
				syndr_arr[i] = 1
				err_arr.append(i+1)

		#print("Syndrome: ", syndr_arr) 
		#print("Error positions: ", err_arr) 

		psi_decoded = psi_noisy.copy()

		err_arr_f = err_arr.copy() #forwards (left-right) direction
		err_arr_b = err_arr[::-1].copy() # backwards (right-left) direction

		def even_or_odd(n):
  			if n % 2 == 0:
    				return 0
  			else:
    				return 1 #as a flag for oddness

		Nerr = len(err_arr)

		#print("Number of errors:", Nerr, " while max is", max_decode, " ?")

		#initializing some arrays needed for decoding

		flips_b = []
		flips_f = []
		x_f = []
		x_b = []

		initialize_zeros = np.zeros(len(psi_initial),dtype = int)
		initialize_ones = np.ones(len(psi_initial),dtype = int)

		flips_ft = []
		flips_bt = []

		if even_or_odd(Nerr) == 1: #odd number of errors
			for i in range(0,Nerr - 1, 2): #0-indexing, pairing up syndrome elements
				a_f = err_arr_f[i]
				b_f = err_arr_f[i+1]
				flips_ft.extend(range(a_f+1, b_f+1)) #forwards: (a,b] position for correction
				b_b = err_arr_b[i]
				a_b = err_arr_b[i+1]
				#print("backwards interval: [",a_b,b_b, "]")
				flips_bt.extend(range(min(a_b,b_b)+1, max(a_b,b_b)+1)) #backwards: same method but syndromes have been paired differently
			for k in range(err_arr_f[-1]+1,len(psi_noisy)+1):
				x_f.append(k)
			for l in range(1, err_arr_b[-1]+1): 
				x_b.append(l)
			flips_ft.extend(x_f)
			flips_bt.extend(x_b)
			#print("Forward method flips suggested: ", flips_ft)
			#print("Backwards method flips suggested: ", flips_bt)	

			candidate_f = np.zeros(len(psi_noisy),dtype = int)
			candidate_b = np.zeros(len(psi_noisy),dtype = int)
	
			for i in flips_ft:
				candidate_f[i-1] = 1 #adjusting back to 0-indexing
			for i in flips_bt:
				candidate_b[i-1] = 1
			#print("noisy candidate f", candidate_f)
			#print("noisy candidate b", candidate_b)
	
			weight_f = len(flips_ft)
			weight_b = len(flips_bt)
			if weight_f > weight_b:
				psi_decoded = psi_decoded^candidate_b #bitwise XOR operation
			if weight_b > weight_f:
				psi_decoded = psi_decoded^candidate_f
			if weight_b == weight_f:
				candidate_r = candidate_f if rng.random() < 0.5 else candidate_b
				psi_decoded = psi_decoded^candidate_r

			#if weight_b == weight_f:
				#candidate = candidate_f if rng.random() < 0.5 else candidate_b
				#psi_decoded = psi_decoded^candidate
		if even_or_odd(Nerr) == 0: #even number of errors
			for i in range(0,Nerr - 1, 2):
				a_f = err_arr_f[i]
				b_f = err_arr_f[i+1]
				flips_f.extend(range(a_f+1, b_f+1)) #still (a,b] intervals
			#print("flips in even case", flips_f)
			for k in flips_f:
				initialize_zeros[k-1] = initialize_zeros[k-1]^1
				initialize_ones[k-1] = initialize_ones[k-1]^1
			#print("from initialized zeros", initialize_zeros)
			#print("from initialized ones", initialize_ones)

			weight_0 = sum(initialize_zeros)
			weight_1 = sum(initialize_ones)

			if weight_0 > weight_1:
				psi_decoded = psi_decoded^initialize_ones
			if weight_1 > weight_0:
				psi_decoded = psi_decoded^initialize_zeros
			if weight_1 == weight_0:
				candidate_r = initialize_ones if rng.random() < 0.5 else initialize_zeros
				psi_decoded = psi_decoded^candidate_r

		#print("decoded psi", psi_decoded)
	
		if sum(psi_decoded) == 0:
			success_arr.append(1)
		else:
			success_arr.append(0)
	print("Success rate is: ", 100*sum(success_arr)/len(success_arr), "for p_i = ", p_i )
	success_arr.clear()
 

