OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[0];
s q[2];
s q[12];
s q[13];
s q[15];
s q[8];
s q[5];
s q[3];
s q[7];
s q[14];
s q[4];
s q[10];
cz q[0], q[12];
cz q[2], q[13];
cz q[15], q[10];
cz q[8], q[7];
cz q[5], q[14];
cz q[3], q[4];
