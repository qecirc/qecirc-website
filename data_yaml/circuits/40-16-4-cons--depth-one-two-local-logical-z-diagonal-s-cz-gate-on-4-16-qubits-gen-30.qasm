OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[5];
s q[4];
s q[20];
s q[18];
s q[19];
s q[17];
s q[36];
s q[37];
id q[39];
cz q[5], q[4];
cz q[20], q[18];
cz q[19], q[17];
cz q[36], q[37];
