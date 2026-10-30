OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[1];
s q[4];
s q[16];
s q[22];
s q[17];
s q[20];
cz q[12], q[19];
cz q[8], q[5];
cz q[7], q[13];
cz q[6], q[23];
cz q[3], q[21];
cz q[2], q[15];
cz q[9], q[14];
cz q[0], q[11];
cz q[10], q[18];
