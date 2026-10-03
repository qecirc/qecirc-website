OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

s q[7];
s q[6];
s q[4];
s q[12];
s q[3];
s q[11];
s q[1];
s q[9];
id q[8];
cz q[7], q[6];
cz q[4], q[12];
cz q[3], q[11];
cz q[1], q[9];
