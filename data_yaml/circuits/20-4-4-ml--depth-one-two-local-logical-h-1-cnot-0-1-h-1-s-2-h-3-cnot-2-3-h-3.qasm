OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[7];
s q[10];
s q[14];
s q[15];
s q[19];
s q[13];
cz q[12], q[6];
cz q[8], q[16];
cz q[4], q[18];
cz q[3], q[9];
cz q[2], q[0];
cz q[1], q[11];
cz q[5], q[17];
