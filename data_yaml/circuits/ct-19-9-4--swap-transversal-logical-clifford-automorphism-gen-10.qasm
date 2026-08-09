OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[13];
z q[9];
z q[5];
z q[4];
z q[15];
cxyz q[7];
czyx q[6];
cxyz q[17];
cxyz q[14];
czyx q[11];
czyx q[18];
cxyz q[12];
id q[0];
czyx q[4];
swap q[12], q[16];
swap q[18], q[12];
swap q[11], q[16];
swap q[8], q[18];
swap q[10], q[16];
swap q[7], q[11];
swap q[15], q[8];
swap q[14], q[10];
swap q[17], q[18];
swap q[6], q[16];
swap q[2], q[8];
swap q[3], q[18];
swap q[4], q[14];
swap q[9], q[6];
swap q[5], q[3];
swap q[13], q[2];
