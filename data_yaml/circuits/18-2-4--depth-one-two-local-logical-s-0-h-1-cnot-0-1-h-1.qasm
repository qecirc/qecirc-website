OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[2];
s q[4];
s q[11];
s q[12];
cz q[10], q[6];
cz q[8], q[17];
cz q[7], q[3];
cz q[5], q[9];
cz q[1], q[14];
cz q[0], q[15];
cz q[16], q[13];
