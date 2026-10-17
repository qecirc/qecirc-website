OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[16], q[18];
cz q[12], q[20];
cz q[10], q[19];
cz q[8], q[21];
cz q[6], q[14];
cz q[22], q[15];
cz q[4], q[23];
cz q[3], q[7];
cz q[2], q[9];
cz q[1], q[11];
cz q[0], q[13];
cz q[5], q[17];
