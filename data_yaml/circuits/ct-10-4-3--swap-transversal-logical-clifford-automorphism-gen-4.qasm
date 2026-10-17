OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[10];

z q[4];
z q[1];
x q[8];
z q[9];
x q[5];
z q[6];
czyx q[7];
czyx q[2];
cxyz q[0];
czyx q[3];
cxyz q[1];
cxyz q[9];
cxyz q[5];
czyx q[6];
swap q[3], q[6];
swap q[0], q[5];
swap q[8], q[9];
swap q[1], q[0];
swap q[2], q[6];
swap q[7], q[8];
