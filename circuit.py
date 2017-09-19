import numpy as np
import pprint
from numpy import kron, sqrt, pi, dot, exp

H_mat = np.matrix([
    [1/sqrt(2), 1/sqrt(2)],
    [1/sqrt(2), -1/sqrt(2)]
])

I = np.identity(2)

CNOT_mat = np.matrix("1 0 0 0 ; 0 1 0 0 ; 0 0 0 1 ; 0 0 1 0")

def Hadamard(H_mat, circuit, qbit):
    order = [0,0,0]
    order[int(qbit)] = 1
    
    if qbit == 0:
        gate = kron(kron(H_mat, I), I)
    elif qbit == 1:
        gate = kron(kron(I, H_mat), I)
    elif qbit == 2:
        gate = kron(kron(I, I), H_mat)
    else: print('Invalid wire')
    
    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new

def CNOT(CNOT_mat, circuit, qbit1, qbit2):
    order = [0,0,0]
    order[int(qbit1)], order[int(qbit2)] = 1, 1
    
    if order[0] == 0:
        gate = kron(I, CNOT_mat)
    else:
        gate = kron(CNOT_mat, I)
        
    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new

def Phase(circuit, shift, qbit):
    order = [0,0,0]
    order[int(qbit)] = 1
    P_mat = np.matrix([
        [1, 0],
        [0, exp(-1j*float(shift))]
    ])
    
    if qbit == 0:
        gate = kron(kron(P_mat, I), I)
    elif qbit == 1:
        gate = kron(kron(I, P_mat), I)
    elif qbit == 2:
        gate = kron(kron(I, I), P_mat)
    else: print('Invalid wire')
    
    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new

def ReadInput(fileName):
    myInput_lines=open(fileName).readlines()
    myInput=[]
    numberOfWires=int(myInput_lines[0])
    for line in myInput_lines[1:]:
        myInput.append(line.split())
    return (numberOfWires,myInput)

num_wires, myInput = ReadInput("circuit_desc.txt")

#print(ReadInput("circuit_desc.txt"))

circuit = []
for gate in myInput:
    if gate[0] == 'H':
        circuit = Hadamard(H_mat, circuit, int(gate[1]))
    elif gate[0] == 'CNOT':
        circuit = CNOT(CNOT_mat, circuit, int(gate[1]), int(gate[2]))
    elif gate[0] == 'P':
        circuit = Phase(circuit, gate[2], int(gate[1]))
pprint.pprint(circuit)

#print(dot([1,0,0,0,0,0,0,0],circuit))
#secondGate=myInput[1][0]
#firstWire=myInput[0][1]
#pprint.pprint(kron([1,0,0,0,0,0,0,0], buildCircuit(H_mat, CNOT_mat, I, P_mat)))