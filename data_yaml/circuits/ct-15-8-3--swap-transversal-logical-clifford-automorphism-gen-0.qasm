OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[9];
z q[4];
czyx q[11];
cxyz q[13];
czyx q[10];
cxyz q[2];
czyx q[3];
cxyz q[7];
swap q[12], q[1];
swap q[14], q[5];
id q[0];
swap q[2], q[3];
swap q[10], q[7];
swap q[9], q[4];
swap q[11], q[13];
