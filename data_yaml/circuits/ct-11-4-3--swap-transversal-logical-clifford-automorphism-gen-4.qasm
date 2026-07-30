OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[2];
x q[9];
z q[10];
z q[1];
z q[4];
z q[6];
czyx q[8];
czyx q[5];
cxyz q[3];
id q[0];
cxyz q[2];
cxyz q[9];
cxyz q[10];
cxyz q[1];
cxyz q[4];
swap q[4], q[6];
swap q[1], q[7];
swap q[2], q[9];
swap q[3], q[2];
swap q[5], q[6];
swap q[8], q[7];
