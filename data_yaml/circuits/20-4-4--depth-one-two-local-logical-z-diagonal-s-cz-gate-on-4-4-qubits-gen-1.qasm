OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

cz q[14], q[4];
cz q[10], q[5];
cz q[7], q[16];
cz q[3], q[13];
cz q[2], q[9];
cz q[1], q[6];
cz q[0], q[18];
cz q[15], q[11];
cz q[8], q[17];
cz q[19], q[12];
