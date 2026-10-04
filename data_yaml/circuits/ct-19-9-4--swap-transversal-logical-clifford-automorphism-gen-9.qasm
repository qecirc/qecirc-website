OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

x q[17];
z q[11];
y q[8];
z q[12];
y q[16];
czyx q[13];
czyx q[9];
czyx q[7];
czyx q[6];
cxyz q[3];
cxyz q[2];
czyx q[14];
czyx q[15];
cxyz q[18];
id q[0];
cxyz q[17];
cxyz q[11];
cxyz q[8];
swap q[18], q[16];
swap q[11], q[16];
swap q[10], q[8];
swap q[2], q[17];
swap q[15], q[11];
swap q[14], q[8];
swap q[4], q[2];
swap q[3], q[8];
swap q[6], q[2];
swap q[7], q[4];
swap q[13], q[15];
swap q[9], q[8];
