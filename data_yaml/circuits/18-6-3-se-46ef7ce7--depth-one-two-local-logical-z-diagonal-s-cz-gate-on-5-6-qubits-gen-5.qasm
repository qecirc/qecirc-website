OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[6];
s q[3];
s q[1];
s q[0];
s q[14];
s q[12];
s q[9];
s q[7];
s q[5];
s q[13];
s q[15];
id q[2];
cz q[8], q[12];
cz q[6], q[14];
cz q[3], q[5];
cz q[1], q[0];
cz q[9], q[13];
cz q[7], q[15];
