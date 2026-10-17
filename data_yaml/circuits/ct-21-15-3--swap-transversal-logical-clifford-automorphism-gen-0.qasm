OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

czyx q[10];
cxyz q[5];
cxyz q[2];
czyx q[13];
swap q[14], q[15];
swap q[11], q[7];
swap q[0], q[17];
swap q[12], q[6];
swap q[9], q[8];
swap q[1], q[18];
swap q[5], q[13];
swap q[10], q[2];
