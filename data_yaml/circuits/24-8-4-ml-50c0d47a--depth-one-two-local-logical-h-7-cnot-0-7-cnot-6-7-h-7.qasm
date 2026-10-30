OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[16];
s q[1];
s q[0];
s q[8];
s q[7];
s q[17];
s q[18];
s q[19];
id q[21];
cz q[16], q[17];
cz q[1], q[0];
cz q[8], q[7];
cz q[18], q[19];
