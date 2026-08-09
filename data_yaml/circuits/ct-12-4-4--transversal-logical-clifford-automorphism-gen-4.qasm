OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[7];
z q[5];
z q[3];
z q[10];
y q[8];
z q[0];
y q[6];
czyx q[4];
czyx q[11];
czyx q[2];
czyx q[9];
czyx q[1];
czyx q[7];
czyx q[5];
czyx q[3];
czyx q[10];
czyx q[8];
czyx q[0];
czyx q[6];
