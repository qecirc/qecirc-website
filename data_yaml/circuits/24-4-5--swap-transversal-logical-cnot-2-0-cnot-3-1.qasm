OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

swap q[16], q[4];
swap q[12], q[3];
swap q[10], q[2];
swap q[8], q[1];
swap q[6], q[0];
swap q[22], q[5];
swap q[15], q[17];
swap q[14], q[13];
swap q[21], q[11];
swap q[19], q[9];
swap q[20], q[7];
swap q[18], q[23];
