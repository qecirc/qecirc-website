OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[6];
z q[1];
x q[7];
z q[0];
z q[10];
z q[8];
z q[5];
y q[9];
z q[3];
czyx q[4];
czyx q[6];
cxyz q[7];
cxyz q[0];
czyx q[10];
czyx q[9];
cxyz q[3];
swap q[5], q[3];
swap q[0], q[10];
swap q[1], q[7];
swap q[2], q[0];
swap q[4], q[7];
swap q[6], q[3];
