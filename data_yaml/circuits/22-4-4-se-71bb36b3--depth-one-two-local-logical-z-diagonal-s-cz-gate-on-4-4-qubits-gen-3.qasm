OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[16];
s q[12];
s q[6];
s q[1];
s q[0];
s q[9];
s q[15];
s q[14];
s q[13];
s q[20];
cz q[8], q[7];
cz q[4], q[2];
cz q[11], q[5];
cz q[3], q[10];
cz q[19], q[18];
cz q[21], q[17];
