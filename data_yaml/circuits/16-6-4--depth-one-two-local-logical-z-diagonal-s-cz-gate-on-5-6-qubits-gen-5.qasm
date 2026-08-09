OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[8];
s q[2];
s q[6];
s q[9];
s q[12];
s q[3];
s q[7];
s q[13];
id q[14];
cz q[8], q[13];
cz q[2], q[7];
cz q[6], q[3];
cz q[9], q[12];
