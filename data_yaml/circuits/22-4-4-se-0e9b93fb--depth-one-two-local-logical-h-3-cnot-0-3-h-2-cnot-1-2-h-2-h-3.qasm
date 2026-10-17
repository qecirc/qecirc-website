OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[18];
s q[16];
s q[12];
s q[5];
s q[3];
s q[11];
s q[9];
s q[1];
s q[6];
s q[14];
s q[17];
s q[19];
s q[21];
s q[20];
cz q[7], q[4];
cz q[2], q[10];
cz q[8], q[0];
cz q[13], q[15];
