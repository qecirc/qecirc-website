OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[4];
s q[15];
s q[13];
s q[7];
cz q[16], q[2];
cz q[12], q[1];
cz q[20], q[0];
cz q[8], q[22];
cz q[6], q[14];
cz q[10], q[18];
cz q[3], q[5];
cz q[19], q[23];
cz q[21], q[17];
cz q[11], q[9];
