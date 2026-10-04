OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

swap q[16], q[10];
swap q[8], q[12];
swap q[0], q[14];
swap q[4], q[1];
swap q[5], q[2];
swap q[6], q[3];
swap q[11], q[17];
swap q[13], q[7];
swap q[15], q[9];
