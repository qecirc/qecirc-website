OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[6];
s q[4];
s q[3];
s q[15];
s q[14];
s q[12];
s q[11];
s q[9];
id q[21];
cz q[6], q[9];
cz q[4], q[3];
cz q[15], q[14];
cz q[12], q[11];
