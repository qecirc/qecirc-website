OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[16];
s q[12];
s q[3];
s q[2];
s q[1];
s q[0];
s q[7];
s q[19];
s q[17];
s q[20];
cz q[8], q[14];
cz q[6], q[21];
cz q[5], q[18];
cz q[4], q[13];
cz q[15], q[22];
cz q[11], q[10];
cz q[9], q[23];
