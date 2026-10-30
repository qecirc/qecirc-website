OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[9];
s q[6];
s q[11];
s q[15];
cz q[10], q[2];
cz q[8], q[16];
cz q[7], q[3];
cz q[5], q[4];
cz q[1], q[13];
cz q[0], q[12];
cz q[17], q[14];
