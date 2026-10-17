OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

s q[8];
s q[6];
s q[5];
s q[2];
s q[1];
s q[0];
s q[7];
s q[4];
s q[13];
s q[17];
s q[14];
s q[15];
id q[20];
cz q[8], q[13];
cz q[6], q[4];
cz q[5], q[7];
cz q[2], q[17];
cz q[1], q[15];
cz q[0], q[14];
