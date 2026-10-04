OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[18];
s q[16];
s q[3];
s q[9];
s q[1];
s q[0];
s q[10];
s q[4];
s q[14];
s q[17];
s q[19];
s q[13];
s q[21];
s q[20];
cz q[12], q[15];
cz q[7], q[5];
cz q[2], q[11];
cz q[6], q[8];
