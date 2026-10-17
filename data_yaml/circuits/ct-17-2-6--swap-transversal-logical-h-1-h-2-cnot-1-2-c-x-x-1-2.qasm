OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[13];
z q[9];
z q[7];
z q[5];
z q[1];
x q[16];
cxyz q[11];
czyx q[4];
cxyz q[3];
czyx q[2];
cxyz q[14];
id q[0];
czyx q[13];
cxyz q[9];
czyx q[7];
cxyz q[5];
czyx q[1];
czyx q[16];
swap q[4], q[3];
swap q[5], q[16];
swap q[7], q[14];
swap q[8], q[3];
swap q[11], q[1];
swap q[13], q[9];
swap q[6], q[5];
swap q[10], q[7];
swap q[12], q[11];
swap q[15], q[9];
