OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[9];

z q[4];
x q[5];
czyx q[7];
czyx q[3];
czyx q[2];
czyx q[8];
czyx q[6];
czyx q[1];
id q[0];
czyx q[4];
czyx q[5];
swap q[2], q[6];
swap q[1], q[5];
swap q[7], q[6];
swap q[3], q[1];
