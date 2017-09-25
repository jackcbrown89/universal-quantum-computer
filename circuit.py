import numpy as np, matplotlib.pyplot as plt
import pprint
from numpy import kron, sqrt, pi, dot, exp, squeeze, cos, sin
from numpy.random import randint


# DECLARE STATIC GATES
H_mat = np.matrix([
    [1/sqrt(2), 1/sqrt(2)],
    [1/sqrt(2), -1/sqrt(2)]
])
I = np.identity(2)
CNOT_mat = np.matrix("1 0 0 0 ; 0 1 0 0 ; 0 0 0 1 ; 0 0 1 0")

def Hadamard(H_mat, circuit, qbit):
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
    P_mat = np.matrix([
        [1, 0],
        [0, exp(1j*float(shift))]
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

def Pauli(circuit, qbit, type):
    if type == 'X':
        Pauli_mat = np.matrix([
        [0, 1],
        [1, 0]
    ])
    elif type == 'Y':
        Pauli_mat = np.matrix([
            [0, -1j],
            [-1j, 0]
        ])
    else:
        Pauli_mat = np.matrix([
            [1, 0],
            [0, -1]
        ])

    if qbit == 0:
        gate = kron(kron(Pauli_mat, I), I)
    elif qbit == 1:
        gate = kron(kron(I, Pauli_mat), I)
    elif qbit == 2:
        gate = kron(kron(I, I), Pauli_mat)
    else:
        print('Invalid wire')

    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new

def Rotate(circuit, qbit, type, theta):
    if type == 'X':
        R_mat = np.matrix([
        [cos(theta/2), -j*sin(theta/2)],
        [-j*sin(theta/2), cos(theta/2)]
    ])
    elif type == 'Y':
        R_mat = np.matrix([
            [cos(theta/2), -1*sin(theta/2)],
            [sin(theta/2), cos(theta/2)]
        ])
    else:
        R_mat = np.matrix([
            [exp(-1j*theta/2), 0],
            [0, exp(1j*theta/2)]
        ])

    if qbit == 0:
        gate = kron(kron(R_mat, I), I)
    elif qbit == 1:
        gate = kron(kron(I, R_mat), I)
    elif qbit == 2:
        gate = kron(kron(I, I), R_mat)
    else:
        print('Invalid wire')

    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new

def genRandCircuit(num_gates):
    gate_nums = [randint(0,3) for x in range(0, num_gates)]
    myInput = []
    
    for gate_num in gate_nums:
        if gate_num == 0:
            myInput.append(['H', randint(0,3)])
        if gate_num == 1:
            firstwire = randint(1,3)
            myInput.append(['CNOT', firstwire, firstwire-1])
        if gate_num == 2:
            myInput.append(['P', randint(0,3), randint(0, 2*pi*100)/100])
    myInput.append(['Measure'])
    return myInput

def ReadDescription(fileName):
    myInput_lines=open(fileName).readlines()
    myInput=[]
    numberOfWires=int(myInput_lines[0])
    for line in myInput_lines[1:]:
        myInput.append(line.split())
    return (numberOfWires,myInput)

def ReadInput(fileName):
    myInput_lines=open(fileName).readlines()
    myInput = []
    for line in myInput_lines:
        myInput.append(complex(float(line.split()[0]), float(line.split()[1])))
    myInput = np.array(myInput, dtype=complex)
    return myInput
    
def measure(result):
    p_list = [x**2 for x in result]
    plt.plot([x for x in range(0,8)], p_list)
    plt.show()

    return

def genCircuit(myInput, inverse):
    circuit = []
    if inverse:
        if myInput[-1] == ['Measure']:
            myInput = myInput[len(myInput)-2::-1]
            myInput.append(['Measure'])
        else: 
            myInput = myInput[::-1]
    print(myInput)
        
    for gate in myInput:
        if gate[0] == 'H':
            circuit = Hadamard(H_mat, circuit, int(gate[1]))
        elif gate[0] == 'PX':
            circuit = Pauli(circuit, int(gate[1]), 'X')
        elif gate[0] == 'PY':
            circuit = Pauli(circuit, int(gate[1]), 'Y')
        elif gate[0] == 'PZ':
            circuit = Pauli(circuit, int(gate[1]), 'Z')
        elif gate[0] == 'RX':
            circuit = Rotate(circuit, int(gate[1]), 'X')
        elif gate[0] == 'RY':
            circuit = Rotate(circuit, int(gate[1]), 'Y')
        elif gate[0] == 'RZ':
            circuit = Rotate(circuit, int(gate[1]), 'Z')
        elif gate[0] == 'CNOT':
            circuit = CNOT(CNOT_mat, circuit, int(gate[1]), int(gate[2]))
        elif gate[0] == 'P':
            if inverse:
                circuit = Phase(circuit, -1*gate[2], int(gate[1]))
            else:
                circuit = Phase(circuit, gate[2], int(gate[1]))
        elif gate[0] == 'Measure':
            result = np.reshape(squeeze(np.asarray(
                dot(inputState,circuit)
                    )), 
                (8,1)
            ).flatten()
            
    return circuit, result

num_wires, myInput = ReadDescription("circuit_desc.txt")    


inputState = np.array(ReadInput('myInputState.txt'))

myInput = genRandCircuit(24)
circuit, result = genCircuit(myInput, False)
inv_circuit = genCircuit(myInput, True)[0]

#inv_circuit = np.linalg.inv(circuit)
print(dot(result, inv_circuit))

import qutip

def graph(vec):
    b=qutip.Bloch()
    up=qutip.basis(2,0)
    down=qutip.basis(2,1)
    b.add_states(vec[0]*up+vec[1]*down)
    b.show()

graph(np.array((result[0], result[1])))