OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[2];
s q[1];
s q[10];
s q[9];
s q[14];
s q[13];
s q[6];
s q[5];
cz q[8], q[15];
cz q[4], q[11];
cz q[0], q[7];
cz q[12], q[3];
