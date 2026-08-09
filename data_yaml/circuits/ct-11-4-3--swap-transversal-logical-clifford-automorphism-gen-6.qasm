OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[8];
z q[5];
z q[3];
x q[9];
z q[1];
x q[4];
x q[6];
z q[7];
cxyz q[2];
id q[0];
czyx q[8];
czyx q[3];
cxyz q[9];
czyx q[1];
cxyz q[7];
swap q[10], q[4];
swap q[6], q[7];
swap q[2], q[4];
swap q[8], q[10];
swap q[1], q[6];
swap q[5], q[4];
swap q[9], q[1];
swap q[3], q[6];
