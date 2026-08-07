OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[14];
s q[9];
s q[19];
s q[1];
s q[0];
s q[2];
s q[18];
s q[10];
s q[20];
s q[13];
s q[23];
s q[15];
id q[21];
cz q[14], q[1];
cz q[9], q[0];
cz q[19], q[2];
cz q[18], q[13];
cz q[10], q[23];
cz q[20], q[15];
