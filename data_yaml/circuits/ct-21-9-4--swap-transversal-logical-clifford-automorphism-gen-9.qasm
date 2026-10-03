OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

czyx q[11];
czyx q[8];
cxyz q[7];
cxyz q[6];
cxyz q[5];
cxyz q[19];
cxyz q[16];
cxyz q[12];
czyx q[17];
czyx q[10];
czyx q[14];
czyx q[18];
swap q[13], q[20];
swap q[15], q[9];
id q[0];
swap q[16], q[10];
swap q[19], q[18];
swap q[5], q[14];
swap q[7], q[17];
swap q[8], q[12];
swap q[11], q[6];
