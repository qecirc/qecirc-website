OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[2];
z q[1];
z q[0];
z q[4];
z q[10];
z q[8];
z q[5];
cxyz q[7];
cxyz q[6];
czyx q[2];
cxyz q[1];
czyx q[0];
czyx q[4];
czyx q[10];
cxyz q[5];
swap q[11], q[6];
swap q[5], q[9];
swap q[0], q[6];
swap q[3], q[10];
swap q[4], q[9];
swap q[7], q[10];
