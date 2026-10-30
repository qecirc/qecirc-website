OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[2];
s q[1];
s q[11];
s q[7];
s q[15];
s q[5];
s q[0];
s q[9];
id q[6];
cz q[2], q[5];
cz q[1], q[7];
cz q[11], q[15];
cz q[0], q[9];
