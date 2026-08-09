OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[5];
s q[20];
s q[11];
s q[22];
cz q[16], q[13];
cz q[12], q[18];
cz q[8], q[17];
cz q[7], q[1];
cz q[6], q[21];
cz q[3], q[0];
cz q[2], q[14];
cz q[4], q[15];
cz q[19], q[9];
cz q[23], q[10];
