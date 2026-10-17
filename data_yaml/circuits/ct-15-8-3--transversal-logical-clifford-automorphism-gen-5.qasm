OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[13];
x q[10];
x q[14];
x q[12];
z q[4];
z q[1];
x q[6];
y q[3];
y q[7];
czyx q[11];
czyx q[9];
czyx q[8];
czyx q[2];
czyx q[5];
id q[0];
czyx q[13];
czyx q[10];
czyx q[14];
czyx q[12];
czyx q[4];
czyx q[1];
czyx q[6];
czyx q[3];
czyx q[7];
