OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[7];
z q[5];
z q[3];
z q[10];
z q[2];
z q[1];
x q[8];
x q[6];
cxyz q[4];
czyx q[7];
cxyz q[5];
czyx q[10];
swap q[0], q[6];
swap q[8], q[0];
swap q[3], q[10];
swap q[1], q[8];
swap q[4], q[3];
swap q[2], q[8];
swap q[5], q[3];
swap q[7], q[4];
