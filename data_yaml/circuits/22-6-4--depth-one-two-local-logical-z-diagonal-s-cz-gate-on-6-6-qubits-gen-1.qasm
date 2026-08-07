OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[10];
s q[4];
s q[3];
s q[8];
s q[7];
s q[17];
s q[14];
s q[13];
id q[21];
cz q[10], q[7];
cz q[4], q[17];
cz q[3], q[14];
cz q[8], q[13];
