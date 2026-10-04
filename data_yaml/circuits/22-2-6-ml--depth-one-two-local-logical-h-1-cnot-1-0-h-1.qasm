OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[22];

xcx q[14], q[2];
xcx q[10], q[8];
xcx q[6], q[19];
xcx q[5], q[16];
xcx q[4], q[21];
xcx q[3], q[17];
xcx q[1], q[18];
xcx q[0], q[7];
xcx q[20], q[13];
xcx q[15], q[12];
xcx q[11], q[9];
