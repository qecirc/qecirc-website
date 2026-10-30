OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[14], q[16];
cz q[9], q[22];
cz q[19], q[12];
cz q[7], q[10];
cz q[6], q[18];
cz q[8], q[20];
cz q[4], q[23];
cz q[3], q[13];
cz q[5], q[15];
cz q[1], q[17];
cz q[0], q[21];
cz q[2], q[11];
