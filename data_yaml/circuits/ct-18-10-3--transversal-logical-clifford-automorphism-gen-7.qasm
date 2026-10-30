OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[7];
x q[12];
y q[17];
y q[11];
x q[16];
y q[14];
z q[8];
x q[15];
z q[9];
z q[6];
czyx q[10];
czyx q[4];
czyx q[13];
czyx q[3];
czyx q[2];
czyx q[5];
id q[0];
czyx q[7];
czyx q[12];
czyx q[17];
czyx q[11];
czyx q[16];
czyx q[14];
czyx q[8];
czyx q[15];
czyx q[9];
czyx q[6];
