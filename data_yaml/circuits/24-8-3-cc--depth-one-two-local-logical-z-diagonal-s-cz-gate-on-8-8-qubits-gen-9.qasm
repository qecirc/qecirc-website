OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

cz q[14], q[1];
cz q[9], q[2];
cz q[19], q[0];
cz q[7], q[16];
cz q[6], q[22];
cz q[8], q[12];
cz q[4], q[17];
cz q[3], q[21];
cz q[5], q[11];
cz q[18], q[15];
cz q[10], q[23];
cz q[20], q[13];
