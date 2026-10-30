OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[10];
s q[4];
s q[3];
s q[1];
s q[11];
s q[7];
s q[9];
s q[8];
cz q[10], q[14];
cz q[4], q[12];
cz q[3], q[15];
cz q[2], q[7];
cz q[1], q[6];
cz q[11], q[13];
cz q[5], q[8];
cz q[0], q[9];
