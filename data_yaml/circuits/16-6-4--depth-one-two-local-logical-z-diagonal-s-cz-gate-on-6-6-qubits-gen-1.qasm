OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[4];
s q[5];
s q[10];
s q[11];
cz q[8], q[6];
cz q[2], q[3];
cz q[1], q[14];
cz q[0], q[15];
cz q[9], q[7];
cz q[12], q[13];
