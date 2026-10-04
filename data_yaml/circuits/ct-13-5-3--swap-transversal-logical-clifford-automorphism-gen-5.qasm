OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[6];
z q[3];
x q[9];
y q[12];
x q[10];
x q[7];
czyx q[4];
czyx q[2];
czyx q[11];
czyx q[5];
id q[0];
czyx q[6];
czyx q[3];
czyx q[9];
czyx q[12];
czyx q[10];
czyx q[7];
swap q[7], q[5];
swap q[9], q[2];
swap q[3], q[12];
swap q[10], q[7];
swap q[4], q[3];
swap q[6], q[9];
