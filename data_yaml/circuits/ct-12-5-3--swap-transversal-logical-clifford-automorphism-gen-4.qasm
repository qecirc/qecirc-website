OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[7];
z q[5];
z q[3];
z q[2];
z q[1];
y q[11];
y q[9];
x q[10];
x q[4];
czyx q[8];
czyx q[6];
id q[0];
cxyz q[7];
czyx q[5];
cxyz q[3];
cxyz q[11];
czyx q[9];
cxyz q[4];
swap q[2], q[8];
swap q[9], q[10];
swap q[1], q[11];
swap q[3], q[2];
swap q[5], q[1];
swap q[7], q[10];
