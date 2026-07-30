OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[7];
z q[4];
z q[3];
y q[11];
z q[2];
y q[6];
z q[13];
z q[9];
z q[1];
z q[5];
z q[8];
czyx q[10];
czyx q[12];
id q[0];
czyx q[4];
czyx q[3];
czyx q[11];
czyx q[2];
czyx q[6];
czyx q[13];
czyx q[9];
czyx q[1];
czyx q[5];
czyx q[8];
swap q[5], q[8];
swap q[13], q[9];
swap q[10], q[11];
swap q[1], q[5];
swap q[2], q[9];
swap q[3], q[10];
