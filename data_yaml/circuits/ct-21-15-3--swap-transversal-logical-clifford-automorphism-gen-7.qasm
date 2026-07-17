OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

czyx q[5];
czyx q[2];
cxyz q[16];
cxyz q[1];
czyx q[20];
czyx q[12];
czyx q[0];
cxyz q[11];
cxyz q[14];
czyx q[3];
cxyz q[6];
cxyz q[18];
czyx q[15];
cxyz q[4];
swap q[15], q[7];
swap q[6], q[18];
swap q[14], q[3];
swap q[17], q[4];
swap q[11], q[7];
swap q[19], q[6];
swap q[8], q[17];
swap q[0], q[15];
swap q[20], q[14];
swap q[16], q[18];
swap q[12], q[17];
swap q[1], q[7];
swap q[2], q[14];
swap q[10], q[19];
swap q[13], q[12];
swap q[5], q[14];
