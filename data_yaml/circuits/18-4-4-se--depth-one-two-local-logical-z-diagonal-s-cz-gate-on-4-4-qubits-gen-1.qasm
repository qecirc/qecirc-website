OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[6];
s q[3];
s q[0];
s q[17];
s q[16];
s q[15];
s q[5];
s q[11];
s q[9];
s q[13];
cz q[8], q[1];
cz q[4], q[12];
cz q[2], q[10];
cz q[14], q[7];
