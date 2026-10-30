OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

z q[12];
z q[2];
x q[20];
cxyz q[8];
cxyz q[7];
cxyz q[4];
cxyz q[16];
czyx q[3];
czyx q[10];
czyx q[14];
cxyz q[19];
cxyz q[9];
cxyz q[13];
czyx q[17];
czyx q[5];
czyx q[15];
czyx q[1];
id q[0];
czyx q[20];
cxyz q[2];
swap q[14], q[9];
swap q[10], q[19];
swap q[16], q[17];
swap q[4], q[15];
swap q[7], q[1];
swap q[8], q[5];
swap q[20], q[13];
swap q[3], q[2];
