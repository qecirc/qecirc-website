OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[10];

z q[2];
x q[8];
z q[9];
z q[6];
czyx q[7];
czyx q[1];
czyx q[0];
cxyz q[3];
czyx q[5];
cxyz q[2];
cxyz q[8];
cxyz q[6];
swap q[3], q[5];
swap q[0], q[3];
swap q[8], q[6];
swap q[9], q[3];
swap q[1], q[6];
swap q[2], q[3];
swap q[4], q[1];
swap q[7], q[1];
