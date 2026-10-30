OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

s q[6];
s q[1];
s q[0];
s q[5];
s q[3];
cz q[8], q[9];
id q[7];
cz q[6], q[1];
cz q[5], q[3];
