OPENQASM 2.0;
include "qelib1.inc";

qreg q[100];
creg rec[42];

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
reset q[97]; h q[97]; // decomposed RX
reset q[98]; h q[98]; // decomposed RX
reset q[99]; h q[99]; // decomposed RX
barrier q;

cx q[58], q[9];
cx q[59], q[6];
cx q[60], q[47];
cx q[61], q[4];
cx q[62], q[38];
cx q[63], q[7];
cx q[64], q[28];
cx q[65], q[25];
cx q[66], q[51];
cx q[67], q[26];
cx q[68], q[42];
cx q[69], q[18];
cx q[70], q[23];
cx q[71], q[29];
cx q[72], q[56];
cx q[73], q[49];
cx q[74], q[52];
cx q[75], q[43];
cx q[76], q[57];
cx q[77], q[34];
cx q[78], q[30];
barrier q;

cx q[58], q[8];
cx q[59], q[7];
cx q[60], q[45];
cx q[61], q[42];
cx q[62], q[9];
cx q[63], q[4];
cx q[64], q[30];
cx q[65], q[56];
cx q[66], q[22];
cx q[67], q[23];
cx q[68], q[41];
cx q[69], q[26];
cx q[70], q[18];
cx q[71], q[11];
cx q[72], q[57];
cx q[73], q[51];
cx q[74], q[46];
cx q[75], q[40];
cx q[76], q[37];
cx q[77], q[52];
cx q[78], q[43];
barrier q;

cx q[58], q[54];
cx q[59], q[22];
cx q[60], q[9];
cx q[61], q[40];
cx q[62], q[4];
cx q[63], q[13];
cx q[64], q[0];
cx q[65], q[26];
cx q[66], q[23];
cx q[67], q[20];
cx q[68], q[18];
cx q[69], q[38];
cx q[70], q[12];
cx q[71], q[30];
cx q[72], q[55];
cx q[73], q[52];
cx q[74], q[47];
cx q[75], q[39];
cx q[76], q[43];
cx q[77], q[33];
cx q[78], q[57];
barrier q;

cx q[58], q[25];
cx q[59], q[49];
cx q[60], q[20];
cx q[61], q[17];
cx q[62], q[36];
cx q[63], q[34];
cx q[64], q[7];
cx q[65], q[55];
cx q[66], q[50];
cx q[67], q[47];
cx q[68], q[16];
cx q[69], q[37];
cx q[70], q[33];
cx q[71], q[23];
cx q[72], q[54];
cx q[73], q[48];
cx q[74], q[57];
cx q[75], q[41];
cx q[76], q[38];
cx q[77], q[43];
cx q[78], q[29];
barrier q;

cx q[58], q[56];
cx q[59], q[51];
cx q[60], q[7];
cx q[61], q[3];
cx q[62], q[2];
cx q[63], q[32];
cx q[64], q[4];
cx q[65], q[24];
cx q[66], q[21];
cx q[67], q[46];
cx q[68], q[17];
cx q[69], q[15];
cx q[70], q[34];
cx q[71], q[18];
cx q[72], q[53];
cx q[73], q[50];
cx q[74], q[45];
cx q[75], q[42];
cx q[76], q[36];
cx q[77], q[31];
cx q[78], q[28];
barrier q;

cx q[60], q[5];
cx q[62], q[15];
cx q[63], q[1];
cx q[64], q[9];
cx q[67], q[19];
cx q[69], q[14];
cx q[70], q[13];
cx q[71], q[26];
cx q[74], q[44];
cx q[76], q[35];
cx q[77], q[32];
cx q[78], q[27];
barrier q;

cx q[64], q[11];
cx q[71], q[10];
cx q[78], q[52];
barrier q;

barrier q;

cz q[79], q[35];
cz q[80], q[27];
cz q[81], q[44];
cz q[82], q[10];
cz q[83], q[23];
cz q[84], q[14];
cz q[85], q[43];
cz q[86], q[52];
cz q[87], q[26];
cz q[88], q[4];
cz q[89], q[7];
cz q[90], q[0];
cz q[91], q[28];
cz q[92], q[45];
cz q[93], q[57];
cz q[94], q[18];
cz q[95], q[11];
cz q[96], q[9];
cz q[97], q[30];
cz q[98], q[34];
cz q[99], q[38];
barrier q;

cz q[79], q[43];
cz q[80], q[52];
cz q[81], q[35];
cz q[82], q[14];
cz q[83], q[10];
cz q[84], q[19];
cz q[85], q[18];
cz q[86], q[23];
cz q[87], q[57];
cz q[88], q[1];
cz q[89], q[0];
cz q[90], q[5];
cz q[91], q[32];
cz q[92], q[7];
cz q[93], q[9];
cz q[94], q[4];
cz q[95], q[20];
cz q[96], q[26];
cz q[97], q[34];
cz q[98], q[47];
cz q[99], q[30];
barrier q;

cz q[79], q[27];
cz q[80], q[44];
cz q[81], q[57];
cz q[82], q[18];
cz q[83], q[12];
cz q[84], q[26];
cz q[85], q[29];
cz q[86], q[46];
cz q[87], q[37];
cz q[88], q[3];
cz q[89], q[1];
cz q[90], q[9];
cz q[91], q[4];
cz q[92], q[32];
cz q[93], q[28];
cz q[94], q[13];
cz q[95], q[7];
cz q[96], q[11];
cz q[97], q[42];
cz q[98], q[52];
cz q[99], q[47];
barrier q;

cz q[79], q[31];
cz q[80], q[48];
cz q[81], q[27];
cz q[82], q[12];
cz q[83], q[19];
cz q[84], q[10];
cz q[85], q[33];
cz q[86], q[29];
cz q[87], q[46];
cz q[88], q[0];
cz q[89], q[5];
cz q[90], q[2];
cz q[91], q[36];
cz q[92], q[52];
cz q[93], q[45];
cz q[94], q[11];
cz q[95], q[13];
cz q[96], q[15];
cz q[97], q[4];
cz q[98], q[23];
cz q[99], q[56];
barrier q;

cz q[79], q[39];
cz q[80], q[31];
cz q[81], q[53];
cz q[82], q[16];
cz q[83], q[21];
cz q[84], q[24];
cz q[85], q[37];
cz q[86], q[33];
cz q[87], q[29];
cz q[88], q[2];
cz q[89], q[6];
cz q[90], q[8];
cz q[91], q[40];
cz q[92], q[28];
cz q[93], q[36];
cz q[94], q[15];
cz q[95], q[23];
cz q[96], q[20];
cz q[97], q[43];
cz q[98], q[30];
cz q[99], q[26];
barrier q;

cz q[85], q[41];
cz q[86], q[50];
cz q[87], q[55];
cz q[91], q[43];
cz q[92], q[49];
cz q[93], q[54];
cz q[94], q[17];
cz q[95], q[22];
cz q[96], q[25];
cz q[97], q[38];
cz q[98], q[51];
cz q[99], q[57];
barrier q;

cz q[97], q[18];
cz q[98], q[7];
cz q[99], q[9];
barrier q;

h q[58]; measure q[58] -> rec[0]; h q[58]; // decomposed MX
h q[59]; measure q[59] -> rec[1]; h q[59]; // decomposed MX
h q[60]; measure q[60] -> rec[2]; h q[60]; // decomposed MX
h q[61]; measure q[61] -> rec[3]; h q[61]; // decomposed MX
h q[62]; measure q[62] -> rec[4]; h q[62]; // decomposed MX
h q[63]; measure q[63] -> rec[5]; h q[63]; // decomposed MX
h q[64]; measure q[64] -> rec[6]; h q[64]; // decomposed MX
h q[65]; measure q[65] -> rec[7]; h q[65]; // decomposed MX
h q[66]; measure q[66] -> rec[8]; h q[66]; // decomposed MX
h q[67]; measure q[67] -> rec[9]; h q[67]; // decomposed MX
h q[68]; measure q[68] -> rec[10]; h q[68]; // decomposed MX
h q[69]; measure q[69] -> rec[11]; h q[69]; // decomposed MX
h q[70]; measure q[70] -> rec[12]; h q[70]; // decomposed MX
h q[71]; measure q[71] -> rec[13]; h q[71]; // decomposed MX
h q[72]; measure q[72] -> rec[14]; h q[72]; // decomposed MX
h q[73]; measure q[73] -> rec[15]; h q[73]; // decomposed MX
h q[74]; measure q[74] -> rec[16]; h q[74]; // decomposed MX
h q[75]; measure q[75] -> rec[17]; h q[75]; // decomposed MX
h q[76]; measure q[76] -> rec[18]; h q[76]; // decomposed MX
h q[77]; measure q[77] -> rec[19]; h q[77]; // decomposed MX
h q[78]; measure q[78] -> rec[20]; h q[78]; // decomposed MX
h q[79]; measure q[79] -> rec[21]; h q[79]; // decomposed MX
h q[80]; measure q[80] -> rec[22]; h q[80]; // decomposed MX
h q[81]; measure q[81] -> rec[23]; h q[81]; // decomposed MX
h q[82]; measure q[82] -> rec[24]; h q[82]; // decomposed MX
h q[83]; measure q[83] -> rec[25]; h q[83]; // decomposed MX
h q[84]; measure q[84] -> rec[26]; h q[84]; // decomposed MX
h q[85]; measure q[85] -> rec[27]; h q[85]; // decomposed MX
h q[86]; measure q[86] -> rec[28]; h q[86]; // decomposed MX
h q[87]; measure q[87] -> rec[29]; h q[87]; // decomposed MX
h q[88]; measure q[88] -> rec[30]; h q[88]; // decomposed MX
h q[89]; measure q[89] -> rec[31]; h q[89]; // decomposed MX
h q[90]; measure q[90] -> rec[32]; h q[90]; // decomposed MX
h q[91]; measure q[91] -> rec[33]; h q[91]; // decomposed MX
h q[92]; measure q[92] -> rec[34]; h q[92]; // decomposed MX
h q[93]; measure q[93] -> rec[35]; h q[93]; // decomposed MX
h q[94]; measure q[94] -> rec[36]; h q[94]; // decomposed MX
h q[95]; measure q[95] -> rec[37]; h q[95]; // decomposed MX
h q[96]; measure q[96] -> rec[38]; h q[96]; // decomposed MX
h q[97]; measure q[97] -> rec[39]; h q[97]; // decomposed MX
h q[98]; measure q[98] -> rec[40]; h q[98]; // decomposed MX
h q[99]; measure q[99] -> rec[41]; h q[99]; // decomposed MX
