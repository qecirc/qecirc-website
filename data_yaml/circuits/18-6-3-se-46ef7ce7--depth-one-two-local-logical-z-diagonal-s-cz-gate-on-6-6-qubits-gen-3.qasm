OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[8];
s q[6];
s q[3];
s q[1];
s q[9];
s q[7];
cz q[10], q[14];
cz q[0], q[2];
cz q[12], q[16];
cz q[17], q[13];
cz q[5], q[4];
cz q[11], q[15];
