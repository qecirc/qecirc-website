OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

xcx q[40], q[44];
xcx q[34], q[32];
xcx q[28], q[38];
xcx q[24], q[46];
xcx q[19], q[45];
xcx q[16], q[33];
xcx q[13], q[39];
xcx q[12], q[47];
xcx q[11], q[41];
xcx q[10], q[25];
xcx q[9], q[29];
xcx q[8], q[35];
xcx q[7], q[31];
xcx q[6], q[37];
xcx q[5], q[42];
xcx q[4], q[27];
xcx q[3], q[17];
xcx q[2], q[22];
xcx q[1], q[20];
xcx q[0], q[14];
xcx q[30], q[18];
xcx q[26], q[23];
xcx q[43], q[21];
xcx q[36], q[15];
