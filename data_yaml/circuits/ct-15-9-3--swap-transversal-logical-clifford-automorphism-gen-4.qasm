OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[8];
x q[10];
z q[13];
z q[1];
x q[7];
x q[6];
x q[14];
x q[11];
z q[12];
cxyz q[4];
czyx q[2];
czyx q[8];
cxyz q[10];
swap q[9], q[12];
swap q[14], q[11];
swap q[6], q[5];
swap q[0], q[9];
swap q[7], q[11];
swap q[1], q[6];
swap q[10], q[13];
swap q[8], q[13];
