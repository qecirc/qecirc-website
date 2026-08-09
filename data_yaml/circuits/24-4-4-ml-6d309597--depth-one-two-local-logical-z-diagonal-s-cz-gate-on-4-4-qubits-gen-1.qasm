OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[12];
s q[8];
s q[6];
s q[5];
s q[4];
s q[3];
s q[11];
s q[9];
s q[21];
s q[18];
s q[23];
s q[20];
id q[22];
cz q[12], q[18];
cz q[8], q[23];
cz q[6], q[3];
cz q[5], q[21];
cz q[4], q[20];
cz q[11], q[9];
