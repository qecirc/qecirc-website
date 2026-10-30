OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[10];
z q[8];
z q[6];
z q[5];
z q[4];
y q[14];
y q[16];
x q[11];
z q[18];
z q[9];
y q[17];
czyx q[15];
czyx q[12];
czyx q[7];
czyx q[3];
czyx q[13];
czyx q[2];
id q[0];
czyx q[10];
czyx q[8];
czyx q[6];
czyx q[5];
czyx q[4];
czyx q[14];
czyx q[16];
czyx q[11];
czyx q[18];
czyx q[9];
czyx q[17];
