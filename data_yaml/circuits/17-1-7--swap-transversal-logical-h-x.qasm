OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

cxyz q[15];
czyx q[14];
czyx q[12];
czyx q[9];
czyx q[7];
cxyz q[6];
cxyz q[4];
czyx q[3];
cxyz q[2];
czyx q[1];
cxyz q[0];
swap q[5], q[16];
swap q[1], q[0];
swap q[4], q[2];
swap q[8], q[7];
swap q[9], q[3];
swap q[13], q[5];
swap q[6], q[4];
swap q[10], q[1];
swap q[12], q[9];
swap q[15], q[8];
