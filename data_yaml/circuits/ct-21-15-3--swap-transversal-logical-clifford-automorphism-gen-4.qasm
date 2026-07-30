OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[21];

cxyz q[10];
swap q[4], q[7];
swap q[3], q[6];
swap q[8], q[11];
swap q[9], q[20];
swap q[13], q[16];
swap q[15], q[7];
swap q[17], q[3];
swap q[0], q[11];
swap q[1], q[9];
swap q[2], q[16];
