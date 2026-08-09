OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

cxyz q[16];
cxyz q[12];
cxyz q[10];
cxyz q[9];
cxyz q[8];
czyx q[7];
czyx q[6];
czyx q[5];
cxyz q[20];
czyx q[17];
czyx q[18];
cxyz q[14];
czyx q[11];
czyx q[21];
czyx q[15];
cxyz q[19];
id q[0];
swap q[15], q[19];
swap q[21], q[19];
swap q[20], q[15];
swap q[11], q[19];
swap q[14], q[21];
swap q[5], q[15];
swap q[18], q[21];
swap q[13], q[11];
swap q[6], q[15];
swap q[10], q[19];
swap q[17], q[18];
swap q[7], q[11];
swap q[8], q[7];
swap q[12], q[17];
swap q[9], q[7];
swap q[16], q[9];
