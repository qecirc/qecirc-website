OPENQASM 2.0;
include "qelib1.inc";

qreg q[37];
creg rec[20];

h q[7];
h q[6];
h q[12];
h q[8];
h q[0];
h q[3];
h q[14];
h q[1];
h q[17];
h q[19];
h q[21];
h q[25];
h q[31];
h q[33];
cx q[7], q[4];
cx q[14], q[13];
cx q[6], q[16];
cx q[17], q[20];
cx q[0], q[2];
cx q[31], q[24];
cx q[12], q[18];
cx q[19], q[23];
cx q[25], q[29];
cx q[33], q[35];
cx q[8], q[11];
cx q[1], q[10];
cx q[7], q[9];
cx q[4], q[16];
cx q[8], q[20];
cx q[2], q[11];
cx q[3], q[0];
cx q[6], q[15];
cx q[31], q[29];
cx q[19], q[22];
cx q[24], q[26];
cx q[12], q[14];
cx q[33], q[34];
cx q[35], q[36];
cx q[16], q[18];
cx q[20], q[23];
cx q[9], q[10];
cx q[8], q[4];
cx q[1], q[0];
cx q[7], q[14];
cx q[13], q[6];
cx q[17], q[22];
cx q[15], q[5];
cx q[26], q[28];
cx q[31], q[32];
cx q[29], q[27];
cx q[24], q[30];
cx q[25], q[11];
cx q[4], q[2];
cx q[0], q[9];
cx q[18], q[22];
cx q[21], q[20];
cx q[3], q[7];
cx q[12], q[15];
cx q[31], q[10];
cx q[26], q[33];
cx q[32], q[36];
cx q[30], q[35];
cx q[14], q[5];
cx q[25], q[34];
measure q[35] -> rec[0];
measure q[36] -> rec[1];
h q[31]; measure q[31] -> rec[2]; h q[31]; // decomposed MX
measure q[33] -> rec[3];
cx q[9], q[19];
cx q[0], q[17];
cx q[6], q[18];
cx q[7], q[21];
cx q[4], q[23];
cx q[2], q[20];
cx q[15], q[22];
cx q[28], q[12];
cx q[24], q[5];
cx q[29], q[34];
measure q[19] -> rec[4];
measure q[17] -> rec[5];
measure q[21] -> rec[6];
measure q[23] -> rec[7];
measure q[22] -> rec[8];
h q[24]; measure q[24] -> rec[9]; h q[24]; // decomposed MX
h q[28]; measure q[28] -> rec[10]; h q[28]; // decomposed MX
measure q[34] -> rec[11];
cx q[26], q[6];
cx q[14], q[18];
cx q[25], q[0];
cx q[30], q[7];
cx q[1], q[20];
cx q[29], q[2];
cx q[27], q[9];
cx q[32], q[4];
measure q[20] -> rec[12];
measure q[18] -> rec[13];
h q[30]; measure q[30] -> rec[14]; h q[30]; // decomposed MX
h q[32]; measure q[32] -> rec[15]; h q[32]; // decomposed MX
h q[26]; measure q[26] -> rec[16]; h q[26]; // decomposed MX
h q[25]; measure q[25] -> rec[17]; h q[25]; // decomposed MX
h q[27]; measure q[27] -> rec[18]; h q[27]; // decomposed MX
h q[29]; measure q[29] -> rec[19]; h q[29]; // decomposed MX
