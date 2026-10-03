OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[10];
s q[6];
s q[1];
s q[11];
s q[7];
s q[17];
s q[2];
s q[14];
id q[12];
cz q[10], q[14];
cz q[6], q[2];
cz q[1], q[7];
cz q[11], q[17];
