OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[8];
s q[6];
s q[3];
s q[2];
s q[0];
s q[10];
s q[5];
s q[7];
s q[13];
s q[9];
s q[11];
s q[14];
id q[12];
cz q[8], q[0];
cz q[6], q[2];
cz q[3], q[13];
cz q[10], q[14];
cz q[5], q[11];
cz q[7], q[9];
