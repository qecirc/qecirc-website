OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[2];
s q[8];
s q[21];
s q[5];
s q[9];
s q[19];
cz q[10], q[13];
cz q[6], q[0];
cz q[4], q[1];
cz q[3], q[7];
cz q[12], q[20];
cz q[11], q[17];
cz q[14], q[16];
cz q[15], q[18];
