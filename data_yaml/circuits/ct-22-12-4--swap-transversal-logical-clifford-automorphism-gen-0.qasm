OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

z q[12];
z q[7];
z q[4];
z q[3];
z q[1];
czyx q[5];
czyx q[2];
cxyz q[11];
czyx q[13];
czyx q[20];
czyx q[19];
cxyz q[9];
cxyz q[15];
czyx q[18];
swap q[17], q[14];
swap q[8], q[6];
cxyz q[12];
cxyz q[3];
cxyz q[1];
swap q[11], q[18];
swap q[2], q[9];
swap q[5], q[15];
swap q[7], q[21];
swap q[16], q[4];
swap q[1], q[19];
swap q[3], q[20];
swap q[12], q[13];
