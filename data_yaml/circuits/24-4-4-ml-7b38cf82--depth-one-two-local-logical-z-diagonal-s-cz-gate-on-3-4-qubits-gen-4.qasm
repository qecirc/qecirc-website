OPENQASM 2.0;
include "qelib1.inc";

qreg q[23];

s q[10];
s q[6];
s q[5];
s q[3];
s q[2];
s q[12];
s q[1];
s q[9];
s q[7];
s q[13];
s q[18];
s q[17];
s q[22];
s q[21];
id q[20];
cz q[10], q[21];
cz q[6], q[12];
cz q[5], q[17];
cz q[3], q[2];
cz q[1], q[18];
cz q[9], q[22];
cz q[7], q[13];
