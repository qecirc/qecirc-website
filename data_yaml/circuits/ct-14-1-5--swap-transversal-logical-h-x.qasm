OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[12];
z q[10];
z q[8];
z q[6];
z q[4];
y q[7];
czyx q[11];
czyx q[9];
czyx q[13];
czyx q[5];
czyx q[3];
id q[0];
czyx q[12];
czyx q[10];
czyx q[8];
czyx q[6];
czyx q[4];
czyx q[7];
swap q[5], q[4];
swap q[11], q[10];
swap q[6], q[4];
swap q[12], q[10];
