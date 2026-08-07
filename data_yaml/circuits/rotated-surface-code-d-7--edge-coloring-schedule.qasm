OPENQASM 2.0;
include "qelib1.inc";

qreg q[97];
creg rec[48];

reset q[49]; h q[49]; // decomposed RX
reset q[50]; h q[50]; // decomposed RX
reset q[51]; h q[51]; // decomposed RX
reset q[52]; h q[52]; // decomposed RX
reset q[53]; h q[53]; // decomposed RX
reset q[54]; h q[54]; // decomposed RX
reset q[55]; h q[55]; // decomposed RX
reset q[56]; h q[56]; // decomposed RX
reset q[57]; h q[57]; // decomposed RX
reset q[58]; h q[58]; // decomposed RX
reset q[59]; h q[59]; // decomposed RX
reset q[60]; h q[60]; // decomposed RX
reset q[61]; h q[61]; // decomposed RX
reset q[62]; h q[62]; // decomposed RX
reset q[63]; h q[63]; // decomposed RX
reset q[64]; h q[64]; // decomposed RX
reset q[65]; h q[65]; // decomposed RX
reset q[66]; h q[66]; // decomposed RX
reset q[67]; h q[67]; // decomposed RX
reset q[68]; h q[68]; // decomposed RX
reset q[69]; h q[69]; // decomposed RX
reset q[70]; h q[70]; // decomposed RX
reset q[71]; h q[71]; // decomposed RX
reset q[72]; h q[72]; // decomposed RX
reset q[73]; h q[73]; // decomposed RX
reset q[74]; h q[74]; // decomposed RX
reset q[75]; h q[75]; // decomposed RX
reset q[76]; h q[76]; // decomposed RX
reset q[77]; h q[77]; // decomposed RX
reset q[78]; h q[78]; // decomposed RX
reset q[79]; h q[79]; // decomposed RX
reset q[80]; h q[80]; // decomposed RX
reset q[81]; h q[81]; // decomposed RX
reset q[82]; h q[82]; // decomposed RX
reset q[83]; h q[83]; // decomposed RX
reset q[84]; h q[84]; // decomposed RX
reset q[85]; h q[85]; // decomposed RX
reset q[86]; h q[86]; // decomposed RX
reset q[87]; h q[87]; // decomposed RX
reset q[88]; h q[88]; // decomposed RX
reset q[89]; h q[89]; // decomposed RX
reset q[90]; h q[90]; // decomposed RX
reset q[91]; h q[91]; // decomposed RX
reset q[92]; h q[92]; // decomposed RX
reset q[93]; h q[93]; // decomposed RX
reset q[94]; h q[94]; // decomposed RX
reset q[95]; h q[95]; // decomposed RX
reset q[96]; h q[96]; // decomposed RX
barrier q;

cx q[49], q[30];
cx q[50], q[35];
cx q[51], q[44];
cx q[53], q[29];
cx q[54], q[34];
cx q[55], q[43];
cx q[56], q[1];
cx q[57], q[33];
cx q[58], q[42];
cx q[59], q[26];
cx q[61], q[32];
cx q[62], q[41];
cx q[63], q[25];
cx q[64], q[2];
cx q[65], q[40];
cx q[66], q[24];
cx q[67], q[14];
cx q[69], q[37];
cx q[70], q[22];
cx q[71], q[13];
cx q[72], q[6];
barrier q;

barrier q;

cz q[73], q[48];
cz q[74], q[46];
cz q[75], q[39];
cz q[76], q[16];
cz q[77], q[7];
cz q[78], q[23];
cz q[79], q[19];
cz q[80], q[10];
cz q[81], q[3];
cz q[82], q[17];
cz q[83], q[8];
cz q[84], q[27];
cz q[85], q[20];
cz q[86], q[11];
cz q[87], q[4];
cz q[88], q[18];
cz q[89], q[9];
cz q[90], q[15];
cz q[91], q[21];
cz q[92], q[12];
cz q[93], q[5];
barrier q;

barrier q;

cx q[49], q[48];
cx q[50], q[46];
cx q[51], q[39];
cx q[53], q[28];
cx q[54], q[16];
cx q[55], q[7];
cx q[56], q[23];
cx q[57], q[19];
cx q[58], q[10];
cx q[59], q[3];
cx q[61], q[31];
cx q[62], q[17];
cx q[63], q[8];
cx q[64], q[27];
cx q[65], q[20];
cx q[66], q[11];
cx q[67], q[4];
cx q[69], q[36];
cx q[70], q[18];
cx q[71], q[9];
cx q[72], q[15];
barrier q;

barrier q;

cz q[73], q[47];
cz q[74], q[45];
cz q[75], q[38];
cz q[76], q[30];
cz q[77], q[35];
cz q[78], q[44];
cz q[79], q[29];
cz q[80], q[34];
cz q[81], q[43];
cz q[82], q[33];
cz q[83], q[42];
cz q[84], q[26];
cz q[85], q[32];
cz q[86], q[41];
cz q[87], q[25];
cz q[88], q[40];
cz q[89], q[24];
cz q[90], q[14];
cz q[91], q[37];
cz q[92], q[22];
cz q[93], q[13];
barrier q;

barrier q;

cx q[49], q[28];
cx q[50], q[16];
cx q[51], q[7];
cx q[52], q[23];
cx q[54], q[19];
cx q[55], q[10];
cx q[56], q[3];
cx q[57], q[31];
cx q[58], q[17];
cx q[59], q[8];
cx q[60], q[27];
cx q[62], q[20];
cx q[63], q[11];
cx q[64], q[4];
cx q[65], q[36];
cx q[66], q[18];
cx q[67], q[9];
cx q[68], q[15];
cx q[70], q[21];
cx q[71], q[12];
cx q[72], q[5];
barrier q;

barrier q;

cz q[76], q[45];
cz q[77], q[38];
cz q[78], q[0];
cz q[79], q[30];
cz q[80], q[35];
cz q[81], q[44];
cz q[82], q[34];
cz q[83], q[43];
cz q[84], q[1];
cz q[85], q[33];
cz q[86], q[42];
cz q[87], q[26];
cz q[88], q[41];
cz q[89], q[25];
cz q[90], q[2];
cz q[91], q[40];
cz q[92], q[24];
cz q[93], q[14];
cz q[94], q[22];
cz q[95], q[13];
cz q[96], q[6];
barrier q;

barrier q;

cx q[49], q[47];
cx q[50], q[45];
cx q[51], q[38];
cx q[52], q[0];
cx q[54], q[30];
cx q[55], q[35];
cx q[56], q[44];
cx q[57], q[29];
cx q[58], q[34];
cx q[59], q[43];
cx q[60], q[1];
cx q[62], q[33];
cx q[63], q[42];
cx q[64], q[26];
cx q[65], q[32];
cx q[66], q[41];
cx q[67], q[25];
cx q[68], q[2];
cx q[70], q[40];
cx q[71], q[24];
cx q[72], q[14];
barrier q;

barrier q;

cz q[76], q[48];
cz q[77], q[46];
cz q[78], q[39];
cz q[79], q[28];
cz q[80], q[16];
cz q[81], q[7];
cz q[82], q[19];
cz q[83], q[10];
cz q[84], q[3];
cz q[85], q[31];
cz q[86], q[17];
cz q[87], q[8];
cz q[88], q[20];
cz q[89], q[11];
cz q[90], q[4];
cz q[91], q[36];
cz q[92], q[18];
cz q[93], q[9];
cz q[94], q[21];
cz q[95], q[12];
cz q[96], q[5];
barrier q;

h q[49]; measure q[49] -> rec[0]; h q[49]; // decomposed MX
h q[50]; measure q[50] -> rec[1]; h q[50]; // decomposed MX
h q[51]; measure q[51] -> rec[2]; h q[51]; // decomposed MX
h q[52]; measure q[52] -> rec[3]; h q[52]; // decomposed MX
h q[53]; measure q[53] -> rec[4]; h q[53]; // decomposed MX
h q[54]; measure q[54] -> rec[5]; h q[54]; // decomposed MX
h q[55]; measure q[55] -> rec[6]; h q[55]; // decomposed MX
h q[56]; measure q[56] -> rec[7]; h q[56]; // decomposed MX
h q[57]; measure q[57] -> rec[8]; h q[57]; // decomposed MX
h q[58]; measure q[58] -> rec[9]; h q[58]; // decomposed MX
h q[59]; measure q[59] -> rec[10]; h q[59]; // decomposed MX
h q[60]; measure q[60] -> rec[11]; h q[60]; // decomposed MX
h q[61]; measure q[61] -> rec[12]; h q[61]; // decomposed MX
h q[62]; measure q[62] -> rec[13]; h q[62]; // decomposed MX
h q[63]; measure q[63] -> rec[14]; h q[63]; // decomposed MX
h q[64]; measure q[64] -> rec[15]; h q[64]; // decomposed MX
h q[65]; measure q[65] -> rec[16]; h q[65]; // decomposed MX
h q[66]; measure q[66] -> rec[17]; h q[66]; // decomposed MX
h q[67]; measure q[67] -> rec[18]; h q[67]; // decomposed MX
h q[68]; measure q[68] -> rec[19]; h q[68]; // decomposed MX
h q[69]; measure q[69] -> rec[20]; h q[69]; // decomposed MX
h q[70]; measure q[70] -> rec[21]; h q[70]; // decomposed MX
h q[71]; measure q[71] -> rec[22]; h q[71]; // decomposed MX
h q[72]; measure q[72] -> rec[23]; h q[72]; // decomposed MX
h q[73]; measure q[73] -> rec[24]; h q[73]; // decomposed MX
h q[74]; measure q[74] -> rec[25]; h q[74]; // decomposed MX
h q[75]; measure q[75] -> rec[26]; h q[75]; // decomposed MX
h q[76]; measure q[76] -> rec[27]; h q[76]; // decomposed MX
h q[77]; measure q[77] -> rec[28]; h q[77]; // decomposed MX
h q[78]; measure q[78] -> rec[29]; h q[78]; // decomposed MX
h q[79]; measure q[79] -> rec[30]; h q[79]; // decomposed MX
h q[80]; measure q[80] -> rec[31]; h q[80]; // decomposed MX
h q[81]; measure q[81] -> rec[32]; h q[81]; // decomposed MX
h q[82]; measure q[82] -> rec[33]; h q[82]; // decomposed MX
h q[83]; measure q[83] -> rec[34]; h q[83]; // decomposed MX
h q[84]; measure q[84] -> rec[35]; h q[84]; // decomposed MX
h q[85]; measure q[85] -> rec[36]; h q[85]; // decomposed MX
h q[86]; measure q[86] -> rec[37]; h q[86]; // decomposed MX
h q[87]; measure q[87] -> rec[38]; h q[87]; // decomposed MX
h q[88]; measure q[88] -> rec[39]; h q[88]; // decomposed MX
h q[89]; measure q[89] -> rec[40]; h q[89]; // decomposed MX
h q[90]; measure q[90] -> rec[41]; h q[90]; // decomposed MX
h q[91]; measure q[91] -> rec[42]; h q[91]; // decomposed MX
h q[92]; measure q[92] -> rec[43]; h q[92]; // decomposed MX
h q[93]; measure q[93] -> rec[44]; h q[93]; // decomposed MX
h q[94]; measure q[94] -> rec[45]; h q[94]; // decomposed MX
h q[95]; measure q[95] -> rec[46]; h q[95]; // decomposed MX
h q[96]; measure q[96] -> rec[47]; h q[96]; // decomposed MX
