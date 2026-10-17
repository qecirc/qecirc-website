OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[8];
s q[0];
s q[10];
s q[4];
cz q[14], q[7];
cz q[6], q[16];
cz q[5], q[3];
cz q[2], q[11];
cz q[1], q[9];
cz q[12], q[17];
cz q[13], q[15];
