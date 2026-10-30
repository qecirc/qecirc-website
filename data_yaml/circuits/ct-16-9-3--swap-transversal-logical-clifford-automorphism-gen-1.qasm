OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[5];
z q[1];
z q[6];
czyx q[9];
czyx q[11];
cxyz q[14];
cxyz q[2];
cxyz q[7];
czyx q[15];
cxyz q[10];
cxyz q[12];
czyx q[4];
czyx q[13];
id q[0];
swap q[12], q[13];
swap q[15], q[10];
swap q[14], q[4];
swap q[11], q[2];
swap q[5], q[6];
swap q[9], q[7];
