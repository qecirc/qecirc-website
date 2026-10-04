OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

xcx q[12], q[28];
xcx q[10], q[24];
xcx q[9], q[20];
xcx q[8], q[16];
xcx q[7], q[3];
xcx q[6], q[41];
xcx q[5], q[36];
xcx q[4], q[32];
xcx q[2], q[27];
xcx q[40], q[23];
xcx q[35], q[19];
xcx q[31], q[15];
xcx q[1], q[26];
xcx q[39], q[22];
xcx q[34], q[18];
xcx q[30], q[14];
xcx q[0], q[25];
xcx q[38], q[21];
xcx q[33], q[17];
xcx q[29], q[13];
xcx q[11], q[44];
xcx q[37], q[45];
xcx q[42], q[46];
xcx q[43], q[47];
