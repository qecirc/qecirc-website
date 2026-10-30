OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[6];
s q[4];
s q[3];
s q[2];
s q[1];
s q[17];
s q[14];
s q[7];
s q[11];
s q[9];
s q[10];
s q[13];
id q[12];
cz q[6], q[9];
cz q[4], q[13];
cz q[3], q[7];
cz q[2], q[14];
cz q[1], q[11];
cz q[17], q[10];
