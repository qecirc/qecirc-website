OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[7];
z q[1];
z q[0];
x q[11];
x q[4];
z q[10];
z q[5];
cxyz q[3];
cxyz q[2];
czyx q[6];
cxyz q[8];
czyx q[7];
cxyz q[11];
czyx q[4];
czyx q[5];
swap q[0], q[10];
swap q[1], q[9];
swap q[8], q[5];
swap q[11], q[6];
swap q[4], q[5];
swap q[3], q[11];
swap q[7], q[6];
swap q[2], q[5];
