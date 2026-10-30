OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

cxyz q[2];
czyx q[11];
swap q[14], q[4];
swap q[9], q[6];
swap q[15], q[3];
swap q[10], q[7];
swap q[8], q[5];
swap q[2], q[11];
