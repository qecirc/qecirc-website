OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[6];
z q[3];
y q[12];
y q[10];
x q[7];
y q[11];
czyx q[4];
czyx q[9];
czyx q[2];
czyx q[5];
id q[0];
czyx q[8];
czyx q[6];
czyx q[3];
czyx q[12];
czyx q[10];
czyx q[7];
czyx q[11];
