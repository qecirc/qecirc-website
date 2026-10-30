OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

s q[1];
s q[7];
s q[9];
s q[8];
s q[10];
s q[5];
cz q[0], q[6];
cz q[2], q[3];
cz q[4], q[11];
