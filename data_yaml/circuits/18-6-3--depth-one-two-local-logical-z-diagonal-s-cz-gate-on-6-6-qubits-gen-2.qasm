OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[10];
s q[3];
s q[2];
s q[11];
s q[4];
s q[5];
cz q[6], q[16];
cz q[8], q[14];
cz q[1], q[13];
cz q[0], q[12];
cz q[7], q[9];
cz q[15], q[17];
