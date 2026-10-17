OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

swap q[6], q[5];
swap q[30], q[29];
swap q[23], q[22];
swap q[15], q[14];
id q[9];
