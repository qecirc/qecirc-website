OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[36];

xcx q[24], q[16];
xcx q[20], q[13];
xcx q[14], q[26];
xcx q[12], q[27];
xcx q[11], q[17];
xcx q[10], q[19];
xcx q[9], q[18];
xcx q[8], q[2];
xcx q[7], q[29];
xcx q[6], q[22];
xcx q[35], q[28];
xcx q[5], q[0];
xcx q[4], q[32];
xcx q[23], q[33];
xcx q[15], q[1];
xcx q[21], q[31];
xcx q[30], q[25];
xcx q[34], q[3];
