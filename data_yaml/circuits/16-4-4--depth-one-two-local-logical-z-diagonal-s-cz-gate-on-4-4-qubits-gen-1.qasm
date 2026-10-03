OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[6];
s q[1];
s q[13];
s q[15];
cz q[10], q[5];
cz q[3], q[9];
cz q[2], q[8];
cz q[14], q[4];
cz q[12], q[0];
cz q[11], q[7];
