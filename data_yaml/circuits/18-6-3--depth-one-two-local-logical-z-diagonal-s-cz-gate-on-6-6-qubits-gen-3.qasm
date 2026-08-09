OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[10];
s q[6];
s q[13];
s q[9];
cz q[3], q[11];
cz q[2], q[15];
cz q[8], q[1];
cz q[0], q[5];
cz q[7], q[14];
cz q[4], q[16];
cz q[12], q[17];
