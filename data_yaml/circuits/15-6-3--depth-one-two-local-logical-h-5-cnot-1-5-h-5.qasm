OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

s q[4];
s q[12];
s q[6];
s q[13];
s q[7];
s q[11];
s q[5];
s q[14];
id q[9];
cz q[4], q[6];
cz q[12], q[14];
cz q[13], q[11];
cz q[7], q[5];
