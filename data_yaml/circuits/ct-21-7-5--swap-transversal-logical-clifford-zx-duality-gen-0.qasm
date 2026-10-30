OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

swap q[19], q[9];
swap q[11], q[14];
swap q[16], q[20];
swap q[0], q[17];
swap q[1], q[12];
swap q[2], q[18];
swap q[3], q[13];
swap q[4], q[9];
swap q[5], q[14];
swap q[6], q[20];
swap q[7], q[17];
swap q[8], q[12];
swap q[10], q[18];
swap q[15], q[13];
