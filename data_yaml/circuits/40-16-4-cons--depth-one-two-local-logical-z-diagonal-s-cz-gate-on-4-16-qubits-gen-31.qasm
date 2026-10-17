OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[4];
s q[3];
s q[18];
s q[16];
s q[17];
s q[15];
s q[37];
s q[38];
id q[39];
cz q[4], q[3];
cz q[18], q[16];
cz q[17], q[15];
cz q[37], q[38];
