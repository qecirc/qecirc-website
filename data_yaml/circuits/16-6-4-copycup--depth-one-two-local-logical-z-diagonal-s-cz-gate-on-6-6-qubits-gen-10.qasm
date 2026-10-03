OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[4];
s q[2];
s q[1];
s q[0];
s q[12];
s q[10];
s q[9];
s q[7];
s q[13];
s q[15];
s q[5];
cz q[8], q[5];
cz q[4], q[12];
cz q[2], q[7];
cz q[1], q[9];
cz q[0], q[13];
cz q[10], q[15];
