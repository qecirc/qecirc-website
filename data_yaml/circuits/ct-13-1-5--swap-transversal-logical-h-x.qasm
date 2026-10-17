OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[11];
z q[9];
z q[7];
z q[5];
z q[3];
y q[6];
czyx q[10];
czyx q[8];
czyx q[12];
czyx q[4];
czyx q[2];
id q[0];
czyx q[11];
czyx q[9];
czyx q[7];
czyx q[5];
czyx q[3];
czyx q[6];
swap q[4], q[3];
swap q[10], q[9];
swap q[5], q[3];
swap q[11], q[9];
