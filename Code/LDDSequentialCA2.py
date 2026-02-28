import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from tqdm import tqdm
from numba import njit

rng = np.random.default_rng()
J = 1

def Nsy_state(N,p):
	psi_i = np.ones(N,dtype = int)
	return np.where(rng.random(N) <= p, -1, psi_i)

def syndrome_calc(psi):
	syndr_arr = []
	for i in range(0, len_psi - 1):
		syndr_arr.append(psi[i]*psi[i+1])
	return syndr_arr

@njit
def s_i(psi_m, psi_p):
	return psi_m*psi_p

@njit
def Decode_step(i, psi, N_s):
	if  i == 0:
		DE_i = 2*J*s_i(psi[0],psi[1])
	elif i == N_s - 1:
		DE_i = 2*J*s_i(psi[N_s - 2], psi[N_s - 1])
	else:
		DE_i = 2*J*(s_i(psi[i-1],psi[i]) + s_i(psi[i],psi[i+1]))
	if DE_i < 0:
		psi[i] *= -1
	elif DE_i > 0:
		pass
	elif DE_i == 0:
		if np.random.rand() < 0.5:
			psi[i] *= -1
	return psi
[0.2,0.3,0.5]

@njit
def Decoding_full(psi, N_s):
	nit = 0
	psi_d = psi.copy()
	while (np.abs(np.sum(psi_d)) != N_s):  
		for i in range(N_s): #should maybe be range of syndrome-1 #rng.permutation(N_s):
			psi_i = Decode_step(i, psi_d, N_s)
			psi_d = psi_i
			nit += 1
	return psi_d, nit

pi_arr = [0.1, 0.2, 0.3, 0.4, 0.5]
Ns_arr = [100,600]
success_p_arr = []
N_mi = 200
average_nit_arr = []
nit_arr = []

i = 0

PN = np.zeros((len(Ns_arr),len(pi_arr)))
for N_i in Ns_arr:
	success_p_arr.clear()
	nit_arr.clear()
	j = 0
	for p_i in pi_arr:
		success_n = 0
		for _ in tqdm(range(N_mi), desc = "sampling for mean"):
			psi_initial = Nsy_state(N_i,p_i)
			psi_final, n_itr  = Decoding_full(psi_initial, N_i)
			if np.sum(psi_final) == N_i:
				success_n += 1
			nit_arr.append(n_itr)
		average_success = success_n/N_mi
		average_nit = np.sum(nit_arr)/N_mi

		PN[i][j] = average_nit

		j += 1
		print("j: ", j)
		average_nit_arr.append(average_nit)
		success_p_arr.append(1 - average_success)
	i += 1
	print("i: ", i)
	plt.scatter(pi_arr, success_p_arr, label = f"N={N_i}")

#plt.scatter(Ns_arr, PN[:][0])
#plt.scatter(np.array(Ns_arr), PN[:,0], label = "p_i = 0.2")
#plt.scatter(np.array(Ns_arr), PN[:,1], label = "p_i = 0.3")
#plt.scatter(np.array(Ns_arr), PN[:,2], label = "p_i = 0.5")

plt.ylabel("N_it/T_dec")
plt.xlabel("Ns")
plt.legend()
plt.show()


'''
spin_hist_arr = np.array(spin_history)
synd_hist_arr = np.array(syndrome_history)

plt.figure(1)

cmap = ListedColormap(["white", "blue"])
im = plt.imshow(spin_hist_arr, interpolation = 'nearest', cmap = cmap, vmin = 0, vmax = 1, aspect='auto')
cbar = plt.colorbar(im, ticks=[0, 1])
cbar.ax.set_yticklabels(['0', '1'])
plt.xlabel("Site index")
plt.xticks(np.arange(N_s))
plt.yticks(np.arange(0, nit+1, 1))
plt.gca().set_xticklabels([])
plt.gca().set_yticklabels([])

plt.ylabel("Decoding step")
plt.title(f"{N_s} state Evolution, p_i = {p_i}, N_i = {nit} ")

plt.show()
'''
plt.figure(2)

'''
cmap = ListedColormap(["white", "blue"])
plt.imshow(synd_hist_arr, aspect='auto')
plt.xlabel("Site index")
plt.xticks(np.arange(N_s - 1))
plt.gca().set_xticklabels([])

plt.ylabel("Decoding step")
plt.title("Syndrome Evolution During Decoding")
'''

#histogram to analyze number of iterations/scalability
'''
n_arr = []
for i in range(100):
	psi_n = Noise(np.zeros(N_s, dtype = int),p_i)
	n_arr.append(Decoding_full(psi_n)[1])

plt.figure(2)
plt.title(f"Histogram: Bit Flip Probability {p_i}")
plt.hist(n_arr, bins = 20)
plt.xlabel("Number of Decoding Iterations")
plt.show()
'''
