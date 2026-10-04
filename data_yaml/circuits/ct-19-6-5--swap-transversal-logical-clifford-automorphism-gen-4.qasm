OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[7];
z q[6];
z q[2];
z q[1];
z q[9];
z q[13];
x q[11];
czyx q[16];
cxyz q[12];
czyx q[10];
cxyz q[18];
czyx q[5];
cxyz q[3];
cxyz q[17];
czyx q[15];
id q[0];
cxyz q[6];
czyx q[2];
czyx q[1];
cxyz q[11];
swap q[5], q[13];
swap q[7], q[17];
swap q[2], q[9];
swap q[3], q[1];
swap q[4], q[11];
swap q[6], q[15];
swap q[18], q[17];
swap q[14], q[13];
swap q[8], q[9];
swap q[10], q[1];
swap q[12], q[11];
swap q[16], q[15];
