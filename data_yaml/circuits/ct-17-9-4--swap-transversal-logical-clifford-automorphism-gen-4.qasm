OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[7];
z q[5];
z q[4];
z q[3];
z q[0];
z q[10];
czyx q[11];
cxyz q[2];
cxyz q[1];
czyx q[15];
czyx q[8];
czyx q[9];
czyx q[6];
swap q[16], q[14];
swap q[12], q[13];
cxyz q[7];
cxyz q[5];
cxyz q[4];
cxyz q[0];
czyx q[10];
swap q[1], q[8];
swap q[2], q[6];
swap q[4], q[9];
swap q[5], q[10];
swap q[7], q[15];
swap q[11], q[0];
