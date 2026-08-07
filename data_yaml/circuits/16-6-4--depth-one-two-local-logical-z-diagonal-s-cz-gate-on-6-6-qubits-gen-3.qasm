OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[4];
s q[0];
s q[15];
s q[12];
s q[3];
s q[7];
s q[11];
cz q[2], q[13];
cz q[1], q[14];
cz q[6], q[9];
cz q[5], q[10];
