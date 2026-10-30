OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[8];

z q[3];
x q[4];
czyx q[6];
czyx q[2];
czyx q[1];
czyx q[7];
czyx q[5];
czyx q[0];
czyx q[3];
czyx q[4];
swap q[1], q[5];
swap q[0], q[4];
swap q[6], q[5];
swap q[2], q[0];
