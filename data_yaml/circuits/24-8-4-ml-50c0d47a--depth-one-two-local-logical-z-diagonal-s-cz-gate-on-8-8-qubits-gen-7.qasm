OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[16], q[23];
cz q[10], q[0];
cz q[6], q[12];
cz q[4], q[14];
cz q[3], q[11];
cz q[2], q[1];
cz q[8], q[5];
cz q[7], q[13];
cz q[22], q[18];
cz q[15], q[9];
cz q[17], q[21];
cz q[19], q[20];
