OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[16];
s q[12];
s q[2];
s q[14];
s q[18];
s q[11];
s q[22];
s q[23];
id q[10];
cz q[16], q[22];
cz q[12], q[11];
cz q[2], q[14];
cz q[18], q[23];
