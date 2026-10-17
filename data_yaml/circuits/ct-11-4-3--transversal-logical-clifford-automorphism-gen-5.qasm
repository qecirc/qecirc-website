OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[5];
z q[2];
x q[9];
z q[10];
y q[4];
x q[7];
czyx q[8];
czyx q[3];
czyx q[1];
czyx q[6];
id q[0];
czyx q[5];
czyx q[2];
czyx q[9];
czyx q[10];
czyx q[4];
czyx q[7];
