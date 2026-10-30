OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[16], q[10];
cz q[12], q[21];
cz q[8], q[19];
cz q[7], q[0];
cz q[6], q[18];
cz q[5], q[11];
cz q[3], q[1];
cz q[2], q[4];
cz q[20], q[22];
cz q[14], q[15];
cz q[13], q[23];
cz q[17], q[9];
