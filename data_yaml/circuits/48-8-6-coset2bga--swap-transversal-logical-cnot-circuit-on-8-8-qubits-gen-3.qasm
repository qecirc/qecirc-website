OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

swap q[26], q[18];
swap q[19], q[6];
swap q[16], q[10];
swap q[15], q[1];
swap q[14], q[13];
swap q[12], q[5];
swap q[9], q[8];
swap q[7], q[0];
swap q[4], q[47];
swap q[2], q[41];
swap q[42], q[22];
swap q[36], q[32];
swap q[38], q[28];
swap q[30], q[34];
swap q[43], q[31];
swap q[40], q[21];
swap q[23], q[46];
swap q[20], q[29];
swap q[44], q[25];
swap q[35], q[24];
id q[17];
