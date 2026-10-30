OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

xcx q[40], q[20];
xcx q[33], q[38];
xcx q[25], q[46];
xcx q[18], q[26];
xcx q[16], q[19];
xcx q[14], q[29];
xcx q[13], q[24];
xcx q[12], q[27];
xcx q[11], q[34];
xcx q[10], q[43];
xcx q[9], q[35];
xcx q[8], q[41];
xcx q[7], q[39];
xcx q[6], q[47];
xcx q[5], q[42];
xcx q[4], q[23];
xcx q[3], q[37];
xcx q[2], q[44];
xcx q[45], q[31];
xcx q[36], q[32];
xcx q[1], q[22];
xcx q[0], q[30];
xcx q[17], q[21];
xcx q[15], q[28];
