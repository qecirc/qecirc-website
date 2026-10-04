OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[16];
s q[8];
s q[11];
s q[2];
s q[5];
s q[19];
s q[21];
s q[20];
id q[17];
cz q[16], q[11];
cz q[8], q[19];
cz q[2], q[21];
cz q[5], q[20];
