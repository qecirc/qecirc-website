OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[0];
z q[3];
cxyz q[2];
czyx q[10];
swap q[5], q[12];
swap q[6], q[11];
swap q[7], q[9];
swap q[8], q[4];
swap q[0], q[3];
swap q[2], q[10];
