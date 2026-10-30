OPENQASM 2.0;
include "qelib1.inc";

qreg q[29];

swap q[4], q[3];
swap q[28], q[27];
swap q[21], q[20];
swap q[13], q[12];
id q[9];
