OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[2];
s q[0];
s q[10];
s q[9];
cz q[8], q[4];
cz q[6], q[14];
cz q[5], q[15];
cz q[1], q[3];
cz q[16], q[11];
cz q[17], q[12];
cz q[7], q[13];
