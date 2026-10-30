OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

cz q[5], q[7];
cz q[2], q[8];
cz q[1], q[9];
cz q[0], q[4];
cz q[6], q[3];
