OPENQASM 2.0;
include "qelib1.inc";

qreg q[43];
creg rec[26];

h q[5];
h q[6];
h q[13];
h q[9];
h q[1];
h q[12];
h q[2];
h q[3];
h q[17];
h q[18];
h q[19];
h q[20];
h q[21];
h q[23];
h q[25];
h q[26];
h q[33];
h q[31];
h q[42];
cx q[12], q[14];
cx q[21], q[24];
cx q[5], q[0];
cx q[31], q[36];
cx q[17], q[22];
cx q[9], q[8];
cx q[6], q[16];
cx q[33], q[32];
cx q[3], q[7];
cx q[23], q[28];
cx q[42], q[39];
cx q[1], q[10];
cx q[13], q[15];
cx q[19], q[27];
cx q[14], q[15];
cx q[0], q[7];
cx q[5], q[11];
cx q[17], q[27];
cx q[24], q[22];
cx q[25], q[21];
cx q[2], q[9];
cx q[26], q[28];
cx q[33], q[31];
cx q[32], q[34];
cx q[8], q[4];
cx q[13], q[6];
cx q[39], q[41];
cx q[36], q[35];
cx q[16], q[14];
cx q[11], q[10];
cx q[7], q[4];
cx q[23], q[24];
cx q[1], q[9];
cx q[25], q[28];
cx q[0], q[6];
cx q[20], q[17];
cx q[3], q[8];
cx q[18], q[26];
cx q[34], q[29];
cx q[31], q[37];
cx q[33], q[38];
cx q[32], q[30];
cx q[12], q[5];
cx q[39], q[40];
cx q[15], q[22];
measure q[22] -> rec[0];
cx q[1], q[21];
cx q[2], q[11];
cx q[9], q[0];
cx q[4], q[26];
cx q[14], q[27];
cx q[13], q[20];
cx q[10], q[25];
cx q[3], q[23];
cx q[6], q[12];
cx q[31], q[40];
cx q[34], q[41];
cx q[35], q[8];
cx q[38], q[42];
cx q[7], q[24];
cx q[30], q[39];
cx q[5], q[17];
measure q[20] -> rec[1];
measure q[17] -> rec[2];
measure q[21] -> rec[3];
measure q[23] -> rec[4];
measure q[24] -> rec[5];
measure q[25] -> rec[6];
measure q[26] -> rec[7];
measure q[27] -> rec[8];
measure q[41] -> rec[9];
measure q[39] -> rec[10];
measure q[42] -> rec[11];
cx q[33], q[2];
cx q[38], q[14];
cx q[37], q[4];
cx q[0], q[18];
cx q[36], q[10];
cx q[35], q[40];
cx q[31], q[1];
cx q[30], q[9];
cx q[11], q[28];
cx q[34], q[3];
cx q[29], q[13];
cx q[6], q[19];
cx q[32], q[12];
measure q[18] -> rec[12];
measure q[19] -> rec[13];
measure q[28] -> rec[14];
measure q[40] -> rec[15];
h q[29]; measure q[29] -> rec[16]; h q[29]; // decomposed MX
h q[30]; measure q[30] -> rec[17]; h q[30]; // decomposed MX
h q[31]; measure q[31] -> rec[18]; h q[31]; // decomposed MX
h q[32]; measure q[32] -> rec[19]; h q[32]; // decomposed MX
h q[33]; measure q[33] -> rec[20]; h q[33]; // decomposed MX
h q[34]; measure q[34] -> rec[21]; h q[34]; // decomposed MX
h q[35]; measure q[35] -> rec[22]; h q[35]; // decomposed MX
h q[36]; measure q[36] -> rec[23]; h q[36]; // decomposed MX
h q[37]; measure q[37] -> rec[24]; h q[37]; // decomposed MX
h q[38]; measure q[38] -> rec[25]; h q[38]; // decomposed MX
