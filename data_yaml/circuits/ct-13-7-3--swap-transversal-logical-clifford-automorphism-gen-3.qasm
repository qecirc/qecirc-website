OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[13];

z q[3];
z q[2];
z q[1];
z q[5];
z q[0];
z q[7];
cxyz q[6];
swap q[12], q[8];
swap q[11], q[7];
swap q[1], q[8];
swap q[2], q[9];
swap q[4], q[11];
swap q[3], q[9];
