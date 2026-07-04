OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[7];
cz q[0], q[1];
cz q[2], q[3];
cz q[1], q[2];
cz q[3], q[4];
cz q[0], q[4];
cx q[5], q[4];
cx q[5], q[2];
cz q[7], q[4];
cz q[5], q[0];
cz q[7], q[1];
cx q[7], q[0];
cz q[5], q[1];
h q[5];
h q[7];
