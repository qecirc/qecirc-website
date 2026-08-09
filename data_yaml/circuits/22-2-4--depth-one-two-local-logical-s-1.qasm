OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[14];
s q[5];
s q[3];
s q[2];
s q[1];
s q[4];
s q[20];
s q[0];
s q[21];
s q[12];
s q[16];
s q[11];
id q[19];
cz q[14], q[12];
cz q[5], q[21];
cz q[3], q[2];
cz q[1], q[4];
cz q[20], q[0];
cz q[16], q[11];
