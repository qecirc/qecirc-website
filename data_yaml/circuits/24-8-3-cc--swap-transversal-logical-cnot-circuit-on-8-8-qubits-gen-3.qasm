OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

swap q[14], q[3];
swap q[9], q[4];
swap q[19], q[5];
swap q[7], q[0];
swap q[6], q[1];
swap q[8], q[2];
swap q[12], q[10];
swap q[22], q[18];
swap q[16], q[20];
swap q[13], q[21];
swap q[23], q[11];
swap q[15], q[17];
