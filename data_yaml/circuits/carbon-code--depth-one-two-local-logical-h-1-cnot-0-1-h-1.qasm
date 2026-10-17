OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

s q[4];
s q[10];
s q[11];
s q[5];
cz q[0], q[8];
cz q[1], q[3];
cz q[6], q[9];
cz q[7], q[2];
