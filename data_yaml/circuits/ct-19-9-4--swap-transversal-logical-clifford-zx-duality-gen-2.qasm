OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

swap q[8], q[12];
swap q[15], q[11];
swap q[10], q[16];
swap q[4], q[18];
id q[0];
swap q[14], q[16];
swap q[17], q[11];
swap q[3], q[8];
swap q[7], q[4];
swap q[13], q[18];
swap q[2], q[17];
swap q[5], q[8];
swap q[6], q[14];
