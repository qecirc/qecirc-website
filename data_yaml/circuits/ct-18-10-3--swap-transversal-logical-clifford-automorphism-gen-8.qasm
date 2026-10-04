OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[10];
z q[7];
z q[4];
y q[13];
z q[3];
z q[17];
z q[11];
y q[14];
z q[8];
x q[5];
z q[15];
czyx q[12];
czyx q[2];
czyx q[16];
czyx q[9];
czyx q[6];
id q[0];
cxyz q[7];
czyx q[4];
czyx q[3];
czyx q[17];
czyx q[11];
czyx q[14];
czyx q[8];
czyx q[5];
czyx q[15];
swap q[2], q[9];
swap q[5], q[15];
swap q[14], q[6];
swap q[16], q[8];
swap q[17], q[2];
swap q[7], q[4];
swap q[11], q[5];
swap q[12], q[6];
swap q[3], q[8];
swap q[10], q[7];
