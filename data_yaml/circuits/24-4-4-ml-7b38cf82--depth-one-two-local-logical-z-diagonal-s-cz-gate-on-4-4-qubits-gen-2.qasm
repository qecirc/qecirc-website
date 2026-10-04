OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[16], q[2];
cz q[10], q[8];
cz q[6], q[11];
cz q[5], q[21];
cz q[4], q[23];
cz q[3], q[22];
cz q[12], q[19];
cz q[1], q[17];
cz q[15], q[0];
cz q[9], q[13];
cz q[14], q[18];
cz q[7], q[20];
