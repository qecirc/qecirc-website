OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[8];
z q[4];
z q[2];
z q[0];
czyx q[13];
cxyz q[1];
cxyz q[7];
czyx q[9];
czyx q[11];
czyx q[3];
swap q[10], q[5];
id q[12];
cxyz q[4];
cxyz q[0];
swap q[7], q[11];
swap q[13], q[1];
swap q[8], q[6];
swap q[0], q[9];
swap q[4], q[3];
