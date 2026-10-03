OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[4];
x q[10];
z q[9];
x q[8];
czyx q[7];
czyx q[5];
czyx q[3];
czyx q[6];
id q[0];
czyx q[4];
czyx q[10];
czyx q[9];
czyx q[8];
swap q[9], q[8];
swap q[4], q[10];
swap q[3], q[8];
swap q[7], q[10];
