OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

czyx q[20];
czyx q[18];
cxyz q[17];
czyx q[14];
cxyz q[13];
cxyz q[12];
czyx q[10];
cxyz q[8];
cxyz q[7];
czyx q[6];
id q[0];
swap q[7], q[21];
swap q[12], q[9];
swap q[13], q[6];
swap q[16], q[8];
swap q[17], q[19];
swap q[10], q[21];
swap q[14], q[12];
swap q[15], q[6];
swap q[18], q[8];
swap q[20], q[17];
