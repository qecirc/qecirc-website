OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[4];
s q[1];
s q[6];
s q[9];
s q[12];
s q[3];
s q[11];
s q[14];
cz q[4], q[9];
cz q[1], q[12];
cz q[6], q[11];
cz q[3], q[14];
