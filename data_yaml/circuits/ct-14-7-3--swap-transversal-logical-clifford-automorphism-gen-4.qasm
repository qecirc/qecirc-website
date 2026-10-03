OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[7];
z q[3];
x q[10];
z q[2];
x q[6];
z q[9];
z q[1];
czyx q[4];
czyx q[11];
cxyz q[13];
id q[0];
czyx q[3];
czyx q[10];
cxyz q[2];
cxyz q[6];
cxyz q[9];
swap q[11], q[13];
swap q[10], q[2];
swap q[3], q[6];
swap q[4], q[9];
