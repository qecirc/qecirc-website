OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

swap q[9], q[7];
swap q[10], q[6];
swap q[11], q[5];
swap q[12], q[4];
swap q[13], q[18];
swap q[15], q[16];
swap q[17], q[14];
id q[0];
