OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

swap q[19], q[0];
swap q[13], q[5];
swap q[8], q[4];
swap q[21], q[2];
swap q[25], q[29];
swap q[17], q[18];
swap q[11], q[12];
swap q[27], q[31];
id q[15];
