OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[3];
s q[2];
s q[1];
s q[4];
cz q[10], q[12];
cz q[6], q[15];
cz q[5], q[11];
cz q[14], q[9];
cz q[0], q[13];
cz q[8], q[7];
