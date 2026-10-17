OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[4];
z q[0];
z q[12];
y q[14];
czyx q[3];
czyx q[1];
cxyz q[8];
czyx q[6];
czyx q[10];
cxyz q[4];
cxyz q[12];
cxyz q[14];
swap q[10], q[14];
swap q[16], q[10];
swap q[6], q[14];
swap q[9], q[10];
swap q[13], q[14];
swap q[12], q[16];
swap q[8], q[13];
swap q[0], q[9];
swap q[2], q[16];
swap q[11], q[12];
swap q[15], q[13];
swap q[1], q[0];
swap q[3], q[16];
swap q[4], q[8];
swap q[5], q[2];
swap q[7], q[2];
