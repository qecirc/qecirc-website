OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[7];
s q[5];
s q[3];
s q[2];
s q[0];
s q[11];
s q[13];
s q[14];
s q[12];
s q[8];
s q[6];
s q[4];
cz q[7], q[2];
cz q[5], q[13];
cz q[3], q[8];
cz q[0], q[14];
cz q[11], q[6];
cz q[12], q[4];
