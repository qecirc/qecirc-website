OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[12];
z q[5];
z q[3];
z q[2];
z q[0];
y q[8];
z q[10];
y q[16];
z q[6];
y q[15];
czyx q[1];
czyx q[11];
cxyz q[14];
cxyz q[13];
cxyz q[12];
cxyz q[5];
cxyz q[3];
czyx q[0];
czyx q[8];
czyx q[10];
czyx q[16];
swap q[11], q[15];
swap q[16], q[13];
swap q[14], q[8];
swap q[2], q[0];
swap q[3], q[10];
swap q[5], q[15];
swap q[4], q[16];
swap q[7], q[14];
swap q[9], q[10];
swap q[12], q[2];
