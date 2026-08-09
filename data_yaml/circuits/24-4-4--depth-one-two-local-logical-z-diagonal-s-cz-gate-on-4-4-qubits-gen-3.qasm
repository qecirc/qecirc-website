OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[18];
s q[14];
s q[4];
s q[22];
cz q[11], q[7];
cz q[5], q[12];
cz q[3], q[21];
cz q[2], q[20];
cz q[1], q[9];
cz q[0], q[6];
cz q[17], q[16];
cz q[10], q[19];
cz q[13], q[8];
cz q[15], q[23];
