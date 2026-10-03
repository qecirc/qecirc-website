OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[11];
z q[9];
z q[7];
z q[6];
z q[5];
y q[15];
y q[17];
x q[12];
z q[19];
z q[10];
y q[18];
czyx q[16];
czyx q[13];
czyx q[8];
czyx q[4];
czyx q[14];
czyx q[3];
sx q[2];
sx q[0];
czyx q[11];
czyx q[9];
czyx q[7];
czyx q[6];
czyx q[5];
czyx q[15];
czyx q[17];
czyx q[12];
czyx q[19];
czyx q[10];
czyx q[18];
swap q[1], q[0];
swap q[2], q[1];
