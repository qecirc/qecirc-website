OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[16], q[5];
cz q[12], q[17];
cz q[8], q[10];
cz q[7], q[21];
cz q[6], q[19];
cz q[3], q[18];
cz q[2], q[20];
cz q[1], q[13];
cz q[4], q[0];
cz q[14], q[9];
cz q[15], q[22];
cz q[11], q[23];
