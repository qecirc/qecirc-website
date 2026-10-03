OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[4];
s q[2];
s q[7];
s q[11];
s q[14];
s q[9];
s q[13];
s q[16];
id q[21];
cz q[4], q[13];
cz q[2], q[11];
cz q[7], q[14];
cz q[9], q[16];
