OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

czyx q[16];
czyx q[9];
czyx q[7];
czyx q[20];
cxyz q[13];
cxyz q[18];
cxyz q[21];
cxyz q[15];
swap q[5], q[19];
swap q[6], q[14];
swap q[10], q[11];
swap q[12], q[17];
id q[0];
swap q[20], q[18];
swap q[7], q[15];
swap q[9], q[13];
swap q[16], q[21];
