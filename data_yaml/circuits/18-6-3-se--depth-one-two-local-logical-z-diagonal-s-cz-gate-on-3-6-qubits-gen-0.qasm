OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[6];
s q[15];
s q[9];
s q[7];
s q[17];
s q[8];
s q[16];
s q[14];
id q[12];
cz q[6], q[15];
cz q[9], q[14];
cz q[7], q[16];
cz q[17], q[8];
