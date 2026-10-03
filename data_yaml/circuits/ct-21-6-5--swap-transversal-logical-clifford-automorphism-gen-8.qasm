OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

z q[18];
z q[16];
z q[14];
z q[7];
z q[4];
czyx q[12];
cxyz q[10];
czyx q[9];
cxyz q[8];
czyx q[6];
cxyz q[5];
cxyz q[3];
czyx q[19];
cxyz q[17];
czyx q[13];
id q[0];
czyx q[18];
cxyz q[16];
swap q[4], q[13];
swap q[5], q[15];
swap q[6], q[17];
swap q[7], q[19];
swap q[8], q[11];
swap q[9], q[3];
swap q[20], q[5];
swap q[10], q[6];
swap q[12], q[7];
swap q[14], q[8];
swap q[16], q[9];
swap q[18], q[4];
