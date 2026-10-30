OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[11];
s q[3];
s q[12];
s q[2];
s q[1];
s q[14];
s q[16];
s q[8];
s q[7];
cz q[6], q[4];
cz q[10], q[13];
cz q[5], q[17];
id q[9];
cz q[2], q[16];
cz q[1], q[8];
cz q[14], q[7];
