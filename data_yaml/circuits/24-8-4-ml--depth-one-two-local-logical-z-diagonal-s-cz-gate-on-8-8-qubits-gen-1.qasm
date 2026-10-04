OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[8];
s q[3];
s q[2];
s q[1];
s q[20];
s q[21];
s q[22];
s q[17];
cz q[16], q[6];
cz q[5], q[4];
cz q[15], q[12];
cz q[14], q[11];
cz q[13], q[10];
cz q[0], q[18];
cz q[7], q[19];
cz q[9], q[23];
