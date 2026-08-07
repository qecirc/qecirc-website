OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

s q[2];
s q[1];
s q[0];
s q[5];
s q[7];
cz q[4], q[2];
cz q[6], q[1];
cz q[8], q[0];
cz q[9], q[5];
cz q[3], q[7];
