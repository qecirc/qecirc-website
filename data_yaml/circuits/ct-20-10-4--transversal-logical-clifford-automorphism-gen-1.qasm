OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[15];
z q[10];
z q[6];
z q[4];
x q[5];
z q[13];
y q[19];
z q[9];
z q[14];
y q[18];
czyx q[12];
czyx q[7];
czyx q[3];
czyx q[2];
czyx q[1];
czyx q[16];
czyx q[17];
czyx q[11];
czyx q[8];
czyx q[0];
czyx q[15];
czyx q[10];
czyx q[6];
czyx q[4];
czyx q[5];
czyx q[13];
czyx q[19];
czyx q[9];
czyx q[14];
czyx q[18];
