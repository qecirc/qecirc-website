OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

cz q[8], q[15];
cz q[6], q[9];
cz q[4], q[7];
cz q[14], q[5];
cz q[2], q[1];
cz q[0], q[13];
cz q[3], q[10];
cz q[12], q[11];
