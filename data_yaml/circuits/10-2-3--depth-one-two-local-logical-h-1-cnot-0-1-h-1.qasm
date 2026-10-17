OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

cz q[4], q[0];
cz q[2], q[9];
cz q[6], q[5];
cz q[1], q[3];
cz q[8], q[7];
