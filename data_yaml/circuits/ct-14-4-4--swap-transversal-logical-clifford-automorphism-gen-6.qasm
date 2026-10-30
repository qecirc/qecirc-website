OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[6];
z q[13];
z q[5];
z q[12];
x q[11];
z q[3];
z q[10];
y q[8];
czyx q[4];
czyx q[2];
id q[0];
czyx q[11];
czyx q[3];
czyx q[10];
czyx q[8];
swap q[13], q[5];
swap q[6], q[12];
swap q[10], q[2];
swap q[3], q[8];
swap q[7], q[5];
swap q[9], q[12];
swap q[11], q[10];
swap q[4], q[3];
