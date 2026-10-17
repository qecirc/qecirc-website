OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[10];
z q[5];
z q[4];
z q[8];
z q[2];
y q[7];
czyx q[9];
czyx q[6];
czyx q[11];
czyx q[3];
id q[0];
czyx q[10];
czyx q[5];
czyx q[4];
czyx q[8];
czyx q[2];
czyx q[7];
swap q[9], q[6];
swap q[8], q[2];
swap q[10], q[6];
swap q[3], q[2];
