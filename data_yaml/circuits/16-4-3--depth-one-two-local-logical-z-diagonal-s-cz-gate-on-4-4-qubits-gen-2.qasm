OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[4];
s q[3];
s q[1];
s q[5];
cz q[10], q[0];
cz q[2], q[7];
cz q[11], q[8];
cz q[15], q[6];
cz q[9], q[12];
cz q[14], q[13];
