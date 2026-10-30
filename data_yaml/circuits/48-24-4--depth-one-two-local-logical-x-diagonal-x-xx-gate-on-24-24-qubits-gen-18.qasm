OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

xcx q[12], q[38];
xcx q[10], q[0];
xcx q[9], q[33];
xcx q[8], q[29];
xcx q[7], q[25];
xcx q[6], q[21];
xcx q[5], q[17];
xcx q[4], q[13];
xcx q[3], q[39];
xcx q[41], q[1];
xcx q[36], q[34];
xcx q[32], q[30];
xcx q[28], q[26];
xcx q[24], q[22];
xcx q[20], q[18];
xcx q[16], q[14];
xcx q[2], q[37];
xcx q[40], q[11];
xcx q[35], q[42];
xcx q[31], q[43];
xcx q[27], q[44];
xcx q[23], q[45];
xcx q[19], q[46];
xcx q[15], q[47];
