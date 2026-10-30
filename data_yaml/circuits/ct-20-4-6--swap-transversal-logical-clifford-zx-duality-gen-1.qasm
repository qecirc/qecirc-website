OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

swap q[14], q[17];
swap q[19], q[18];
swap q[8], q[6];
swap q[9], q[7];
swap q[0], q[14];
swap q[1], q[19];
swap q[2], q[17];
swap q[3], q[18];
swap q[10], q[8];
swap q[11], q[9];
swap q[12], q[6];
swap q[13], q[7];
swap q[4], q[14];
swap q[5], q[19];
swap q[15], q[8];
swap q[16], q[9];
