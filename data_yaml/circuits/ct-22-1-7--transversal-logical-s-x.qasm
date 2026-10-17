OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

czyx q[20];
czyx q[19];
czyx q[18];
czyx q[17];
czyx q[16];
czyx q[15];
czyx q[14];
czyx q[13];
czyx q[12];
czyx q[11];
czyx q[10];
czyx q[9];
czyx q[8];
czyx q[7];
czyx q[6];
czyx q[5];
czyx q[21];
id q[0];
