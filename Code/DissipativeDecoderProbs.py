import numpy as np
import scipy as sp
import math 

rng = np.random.default_rng()

N =  20 
p_i = 0.7

psi_initial = (np.random.random(N) <= p_i).astype(int)
print("Initial random psi:", psi_initial)
#np.random.random(n) generatesd random floats between 0 and 1
#.astype(int) converts true to 1 and false to 0.

max_decode = math.floor((len(psi_initial)-1)/2)

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
			if np.array_equal(init_arr, np.array([0,1])):
				Eloc_arr.append(1)
			if np.array_equal(init_arr, np.array([1,1])) or np.array_equal(init_arr, np.array([1,0])):
				Eloc_arr.append(0)
		elif i == Ns - 1:
			sN = syndromes[Ns - 1]
			sN1 = syndromes[Ns - 2]
			sN2 = syndromes[Ns - 3]
			if sN != sN1:
				init_arr[0] = 1
			if sN != sN2:
				init_arr[1] = 1
			
			if np.array_equal(init_arr, np.array([1,1])) or np.array_equal(init_arr, np.array([1,0])): #possibly rethink this one, but I think it will converge
				if rng.random() < 0.5:
					Eloc_arr.append(Npsi-1)
			if np.array_equal(init_arr,np.array([0,1])):
				if rng.random() < 0.5:
					Eloc_arr.append(Npsi-2) #flip second to last
		else:
			si = syndromes[i]
			sim = syndromes[i-1]
			sip = syndromes[i+1]
			if si != sim:
				init_arr[0] = 1
			if si != sip:
				init_arr[1] = 1
			if np.array_equal(init_arr, np.array([1,0])):
				if rng.random() < 0.5:
					Eloc_arr.append(i)
			if np.array_equal(init_arr, np.array([0,1])) or np.array_equal(init_arr, np.array([1,1])):
				if rng.random() < 0.5:
					Eloc_arr.append(i+1)
			if np.array_equal(init_arr, np.array([1,1])):
				if rng.random() < 0.5:
					Eloc_arr.append(i+1)
		init_arr = np.zeros(2, dtype = int) #restoring init_arr
	
	Eloc_ammend = set(Eloc_arr)
	print("error locations", Eloc_ammend)
	return Eloc_ammend

def Denoise(psi,Errloc):
	psi_decode = psi.copy()
	for i in Errloc:
		psi_decode[i] = psi_decode[i]^1
	return psi_decode

def Syndrome(psi):
	len_psi = len(psi)
	syndr_arr = np.zeros(len_psi - 1, dtype = int)
	for i in range(0, len_psi - 1): #0-indexing here and syndrome length
        	if psi[i] != psi[i+1]: #flag domain walls with 1
                	syndr_arr[i] = 1
	print("Syndrome Array:", syndr_arr)
	return syndr_arr

def Energy(psi):
	E_i = []
	syndr_arr = Syndrome(psi)
	for i in range(0,len(syndr_arr)):
		E_i.append(syndr_arr[i])
	E_total = np.sum(E_i)
	return E_total

def Diss_step(psi_init):
	psi_i = psi_init.copy()
	synd_i = Syndrome(psi_i)
	Energy_i = Energy(psi_i)
	psi_denoised = Denoise(psi_i,ECupdate(psi_i,synd_i))
	Energy_f = Energy(psi_denoised)
	if Energy_i >= Energy_f:
		print("Energy is:", Energy_i, "vs", Energy_f,"modification accepted")
		return psi_denoised
	else:
		print("Energy is:", Energy_i, "vs", Energy_f,"modification rejected")
		return psi_i

trial_state = psi_initial
for i in range(500):
	trial_state = Diss_step(trial_state)
	print("trial step:", trial_state, "with energy", Energy(trial_state))
#print("trial: ", ECupdate(trial1,syn1), "for noisy state:", trial1, "and denoisied state is:", Denoise(trial1, ECupdate(trial1,syn1)))

