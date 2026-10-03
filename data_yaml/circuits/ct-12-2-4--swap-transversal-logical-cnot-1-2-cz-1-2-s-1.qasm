OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[10];
z q[9];
z q[4];
x q[8];
x q[7];
czyx q[6];
czyx q[11];
cxyz q[3];
czyx q[2];
id q[0];
cxyz q[10];
cxyz q[4];
swap q[11], q[3];
swap q[5], q[8];
swap q[4], q[2];
swap q[10], q[6];
