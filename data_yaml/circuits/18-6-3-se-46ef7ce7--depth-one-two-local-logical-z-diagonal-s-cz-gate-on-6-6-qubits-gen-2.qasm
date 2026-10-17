OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[6];
s q[14];
s q[9];
s q[13];
cz q[10], q[17];
cz q[8], q[3];
cz q[1], q[7];
cz q[0], q[15];
cz q[12], q[5];
cz q[16], q[2];
cz q[11], q[4];
