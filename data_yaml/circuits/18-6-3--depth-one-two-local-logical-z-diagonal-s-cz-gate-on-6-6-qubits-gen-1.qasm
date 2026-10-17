OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

cz q[10], q[8];
cz q[6], q[7];
cz q[3], q[1];
cz q[2], q[16];
cz q[0], q[4];
cz q[15], q[5];
cz q[11], q[9];
cz q[13], q[12];
cz q[14], q[17];
