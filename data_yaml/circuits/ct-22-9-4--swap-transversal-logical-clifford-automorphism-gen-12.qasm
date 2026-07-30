OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

cxyz q[16];
czyx q[12];
cxyz q[10];
czyx q[8];
cxyz q[6];
czyx q[5];
cxyz q[20];
cxyz q[13];
czyx q[18];
czyx q[21];
cxyz q[15];
id q[0];
swap q[15], q[19];
swap q[20], q[14];
swap q[6], q[17];
swap q[7], q[21];
swap q[9], q[8];
swap q[18], q[19];
swap q[5], q[14];
swap q[10], q[9];
swap q[12], q[17];
swap q[16], q[21];
