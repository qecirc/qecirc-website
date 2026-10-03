OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[56];

xcx q[44], q[48];
xcx q[37], q[50];
xcx q[34], q[42];
xcx q[32], q[49];
xcx q[30], q[43];
xcx q[28], q[51];
xcx q[54], q[41];
xcx q[22], q[23];
xcx q[18], q[25];
xcx q[17], q[20];
xcx q[16], q[24];
xcx q[15], q[21];
xcx q[14], q[26];
xcx q[27], q[19];
xcx q[12], q[38];
xcx q[11], q[45];
xcx q[10], q[55];
xcx q[9], q[29];
xcx q[8], q[31];
xcx q[7], q[33];
xcx q[13], q[35];
xcx q[5], q[39];
xcx q[4], q[46];
xcx q[3], q[53];
xcx q[2], q[36];
xcx q[1], q[40];
xcx q[0], q[47];
xcx q[6], q[52];
