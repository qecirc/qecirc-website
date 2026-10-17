OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

czyx q[17];
czyx q[14];
czyx q[11];
czyx q[10];
cxyz q[9];
cxyz q[8];
cxyz q[7];
cxyz q[6];
cxyz q[5];
czyx q[4];
czyx q[3];
id q[0];
swap q[6], q[3];
swap q[8], q[19];
swap q[9], q[4];
swap q[12], q[7];
swap q[14], q[5];
swap q[10], q[8];
swap q[15], q[3];
swap q[16], q[14];
swap q[17], q[12];
swap q[18], q[4];
