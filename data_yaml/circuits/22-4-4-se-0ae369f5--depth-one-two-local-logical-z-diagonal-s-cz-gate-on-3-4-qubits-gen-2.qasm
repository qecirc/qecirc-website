OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[4];
s q[2];
s q[1];
s q[0];
s q[15];
s q[10];
s q[5];
s q[7];
s q[13];
s q[9];
s q[11];
s q[14];
id q[12];
cz q[4], q[10];
cz q[2], q[11];
cz q[1], q[5];
cz q[0], q[9];
cz q[15], q[7];
cz q[13], q[14];
