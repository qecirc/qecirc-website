OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[12], q[7];
cz q[10], q[8];
cz q[6], q[0];
cz q[4], q[1];
cz q[2], q[18];
cz q[23], q[21];
cz q[19], q[14];
cz q[17], q[15];
cz q[22], q[9];
cz q[20], q[11];
cz q[16], q[3];
cz q[13], q[5];
