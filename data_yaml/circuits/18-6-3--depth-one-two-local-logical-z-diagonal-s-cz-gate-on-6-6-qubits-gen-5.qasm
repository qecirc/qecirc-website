OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[6];
s q[3];
s q[2];
s q[0];
s q[7];
s q[13];
s q[5];
s q[16];
s q[9];
cz q[10], q[6];
cz q[3], q[8];
cz q[2], q[11];
cz q[1], q[16];
cz q[0], q[14];
cz q[7], q[4];
cz q[15], q[5];
cz q[13], q[17];
cz q[12], q[9];
