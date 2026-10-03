OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[10];
z q[8];
z q[6];
z q[4];
z q[2];
z q[0];
z q[11];
swap q[3], q[13];
swap q[5], q[1];
czyx q[10];
czyx q[8];
czyx q[6];
czyx q[4];
czyx q[2];
czyx q[0];
czyx q[11];
swap q[7], q[5];
swap q[12], q[13];
swap q[0], q[11];
swap q[6], q[4];
swap q[8], q[0];
swap q[10], q[4];
