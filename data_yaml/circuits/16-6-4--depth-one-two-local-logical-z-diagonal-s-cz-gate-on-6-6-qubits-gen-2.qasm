OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[2];
s q[6];
s q[9];
s q[12];
s q[3];
s q[7];
s q[13];
cz q[4], q[14];
cz q[1], q[11];
cz q[0], q[10];
cz q[5], q[15];
