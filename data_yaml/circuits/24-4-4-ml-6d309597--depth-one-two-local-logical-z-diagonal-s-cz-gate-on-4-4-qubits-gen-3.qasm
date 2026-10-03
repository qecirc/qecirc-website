OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[0];
s q[7];
s q[19];
s q[17];
cz q[16], q[1];
cz q[12], q[8];
cz q[6], q[4];
cz q[5], q[13];
cz q[3], q[10];
cz q[2], q[23];
cz q[15], q[20];
cz q[11], q[21];
cz q[9], q[22];
cz q[14], q[18];
