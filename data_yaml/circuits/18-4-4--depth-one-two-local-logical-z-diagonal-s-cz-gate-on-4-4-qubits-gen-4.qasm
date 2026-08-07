OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

s q[8];
s q[6];
s q[5];
s q[4];
s q[2];
s q[1];
s q[14];
s q[16];
s q[15];
s q[3];
s q[10];
s q[11];
id q[13];
cz q[8], q[2];
cz q[6], q[15];
cz q[5], q[3];
cz q[4], q[10];
cz q[1], q[11];
cz q[14], q[16];
