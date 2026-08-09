OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[10];
s q[23];
s q[22];
s q[15];
s q[14];
s q[12];
s q[11];
s q[13];
id q[21];
cz q[10], q[13];
cz q[23], q[22];
cz q[15], q[14];
cz q[12], q[11];
