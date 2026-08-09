OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[8];
s q[2];
s q[1];
s q[0];
s q[14];
s q[18];
cz q[12], q[13];
cz q[6], q[10];
cz q[4], q[19];
cz q[3], q[9];
cz q[17], q[11];
cz q[7], q[16];
cz q[15], q[5];
