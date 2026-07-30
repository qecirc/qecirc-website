OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[13];
z q[10];
z q[8];
z q[6];
z q[4];
z q[2];
z q[14];
swap q[3], q[12];
swap q[5], q[1];
id q[0];
czyx q[13];
czyx q[10];
czyx q[8];
czyx q[6];
czyx q[4];
czyx q[2];
czyx q[14];
swap q[7], q[5];
swap q[11], q[12];
swap q[6], q[4];
swap q[8], q[14];
swap q[10], q[4];
swap q[13], q[8];
