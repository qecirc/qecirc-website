OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[2];
z q[4];
x q[10];
z q[6];
z q[5];
x q[9];
czyx q[7];
cxyz q[3];
czyx q[1];
czyx q[11];
cxyz q[2];
czyx q[4];
cxyz q[6];
cxyz q[9];
swap q[1], q[8];
swap q[3], q[10];
swap q[11], q[6];
swap q[2], q[8];
swap q[7], q[3];
swap q[0], q[6];
