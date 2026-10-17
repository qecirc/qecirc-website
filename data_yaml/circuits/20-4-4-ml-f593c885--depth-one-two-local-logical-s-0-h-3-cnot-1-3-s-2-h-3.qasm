OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[4];
s q[3];
s q[1];
s q[19];
s q[17];
s q[7];
cz q[12], q[8];
cz q[6], q[16];
cz q[2], q[18];
cz q[0], q[5];
cz q[15], q[13];
cz q[9], q[10];
cz q[14], q[11];
