OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[4];
s q[2];
s q[1];
s q[3];
s q[6];
s q[15];
s q[5];
cz q[8], q[15];
cz q[4], q[3];
cz q[2], q[5];
cz q[1], q[6];
