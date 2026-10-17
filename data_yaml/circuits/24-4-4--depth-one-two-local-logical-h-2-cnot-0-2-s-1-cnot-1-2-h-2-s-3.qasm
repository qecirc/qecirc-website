OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[1];
s q[20];
s q[6];
s q[19];
cz q[18], q[9];
cz q[14], q[10];
cz q[11], q[15];
cz q[7], q[13];
cz q[5], q[21];
cz q[4], q[2];
cz q[3], q[17];
cz q[0], q[22];
cz q[12], q[16];
cz q[8], q[23];
