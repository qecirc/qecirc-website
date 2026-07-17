OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[6];
z q[4];
z q[11];
x q[10];
x q[9];
czyx q[5];
cxyz q[12];
swap q[1], q[7];
id q[0];
czyx q[6];
cxyz q[4];
swap q[2], q[9];
swap q[3], q[7];
swap q[10], q[2];
swap q[4], q[11];
swap q[6], q[12];
swap q[5], q[11];
swap q[8], q[6];
