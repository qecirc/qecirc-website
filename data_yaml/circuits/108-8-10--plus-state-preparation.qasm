OPENQASM 2.0;
include "qelib1.inc";

qreg q[108];

reset q[84];
reset q[80];
reset q[64];
reset q[57];
reset q[56];
reset q[55];
reset q[54];
reset q[53];
reset q[49];
reset q[44];
reset q[43];
reset q[40];
reset q[39];
reset q[38];
reset q[37];
reset q[36];
reset q[35];
reset q[34];
reset q[31];
reset q[30];
reset q[29];
reset q[28];
reset q[27];
reset q[26];
reset q[25];
reset q[24];
reset q[23];
reset q[22];
reset q[21];
reset q[20];
reset q[19];
reset q[18];
reset q[17];
reset q[16];
reset q[98];
reset q[85];
reset q[15];
reset q[14];
reset q[13];
reset q[12];
reset q[11];
reset q[10];
reset q[8];
reset q[7];
reset q[6];
reset q[5];
reset q[4];
reset q[3];
reset q[32];
reset q[72];
reset q[9]; h q[9]; // decomposed RX
reset q[48]; h q[48]; // decomposed RX
reset q[45]; h q[45]; // decomposed RX
reset q[2]; h q[2]; // decomposed RX
reset q[33]; h q[33]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[81]; h q[81]; // decomposed RX
reset q[86]; h q[86]; // decomposed RX
reset q[107]; h q[107]; // decomposed RX
reset q[99]; h q[99]; // decomposed RX
reset q[102]; h q[102]; // decomposed RX
reset q[79]; h q[79]; // decomposed RX
reset q[71]; h q[71]; // decomposed RX
reset q[87]; h q[87]; // decomposed RX
reset q[106]; h q[106]; // decomposed RX
reset q[101]; h q[101]; // decomposed RX
reset q[104]; h q[104]; // decomposed RX
reset q[77]; h q[77]; // decomposed RX
reset q[41]; h q[41]; // decomposed RX
reset q[47]; h q[47]; // decomposed RX
reset q[83]; h q[83]; // decomposed RX
reset q[73]; h q[73]; // decomposed RX
reset q[88]; h q[88]; // decomposed RX
reset q[105]; h q[105]; // decomposed RX
reset q[100]; h q[100]; // decomposed RX
reset q[103]; h q[103]; // decomposed RX
reset q[78]; h q[78]; // decomposed RX
reset q[46]; h q[46]; // decomposed RX
reset q[42]; h q[42]; // decomposed RX
reset q[82]; h q[82]; // decomposed RX
reset q[94]; h q[94]; // decomposed RX
reset q[76]; h q[76]; // decomposed RX
reset q[50]; h q[50]; // decomposed RX
reset q[91]; h q[91]; // decomposed RX
reset q[70]; h q[70]; // decomposed RX
reset q[96]; h q[96]; // decomposed RX
reset q[66]; h q[66]; // decomposed RX
reset q[61]; h q[61]; // decomposed RX
reset q[62]; h q[62]; // decomposed RX
reset q[90]; h q[90]; // decomposed RX
reset q[69]; h q[69]; // decomposed RX
reset q[97]; h q[97]; // decomposed RX
reset q[65]; h q[65]; // decomposed RX
reset q[58]; h q[58]; // decomposed RX
reset q[59]; h q[59]; // decomposed RX
reset q[93]; h q[93]; // decomposed RX
reset q[75]; h q[75]; // decomposed RX
reset q[51]; h q[51]; // decomposed RX
reset q[89]; h q[89]; // decomposed RX
reset q[68]; h q[68]; // decomposed RX
reset q[95]; h q[95]; // decomposed RX
reset q[67]; h q[67]; // decomposed RX
reset q[60]; h q[60]; // decomposed RX
reset q[63]; h q[63]; // decomposed RX
reset q[92]; h q[92]; // decomposed RX
reset q[74]; h q[74]; // decomposed RX
reset q[52]; h q[52]; // decomposed RX
cx q[106], q[32];
cx q[50], q[4];
cx q[62], q[11];
cx q[67], q[72];
cx q[0], q[5];
cx q[66], q[6];
cx q[105], q[7];
cx q[100], q[8];
cx q[88], q[10];
cx q[76], q[13];
cx q[102], q[85];
cx q[51], q[26];
cx q[47], q[3];
cx q[94], q[12];
cx q[87], q[17];
cx q[79], q[22];
cx q[65], q[31];
cx q[2], q[16];
cx q[60], q[19];
cx q[74], q[35];
cx q[95], q[80];
cx q[81], q[20];
cx q[70], q[36];
cx q[63], q[62];
cx q[1], q[32];
cx q[73], q[11];
cx q[50], q[98];
cx q[61], q[72];
cx q[59], q[5];
cx q[106], q[7];
cx q[48], q[10];
cx q[45], q[13];
cx q[86], q[85];
cx q[105], q[18];
cx q[0], q[21];
cx q[100], q[28];
cx q[51], q[49];
cx q[102], q[3];
cx q[94], q[8];
cx q[88], q[14];
cx q[107], q[17];
cx q[47], q[22];
cx q[79], q[34];
cx q[76], q[39];
cx q[95], q[15];
cx q[91], q[26];
cx q[60], q[53];
cx q[74], q[64];
cx q[66], q[80];
cx q[96], q[73];
cx q[63], q[4];
cx q[32], q[6];
cx q[9], q[11];
cx q[42], q[98];
cx q[78], q[50];
cx q[67], q[1];
cx q[77], q[10];
cx q[68], q[13];
cx q[45], q[85];
cx q[62], q[18];
cx q[61], q[23];
cx q[0], q[30];
cx q[59], q[51];
cx q[92], q[105];
cx q[2], q[5];
cx q[94], q[25];
cx q[86], q[28];
cx q[82], q[3];
cx q[65], q[26];
cx q[91], q[38];
cx q[75], q[53];
cx q[58], q[73];
cx q[101], q[4];
cx q[87], q[6];
cx q[106], q[11];
cx q[9], q[12];
cx q[48], q[98];
cx q[96], q[24];
cx q[50], q[31];
cx q[69], q[32];
cx q[100], q[78];
cx q[46], q[1];
cx q[45], q[17];
cx q[42], q[54];
cx q[77], q[102];
cx q[0], q[105];
cx q[88], q[62];
cx q[47], q[61];
cx q[68], q[51];
cx q[79], q[67];
cx q[107], q[63];
cx q[81], q[25];
cx q[86], q[40];
cx q[59], q[44];
cx q[99], q[4];
cx q[106], q[13];
cx q[9], q[16];
cx q[101], q[18];
cx q[48], q[21];
cx q[50], q[22];
cx q[73], q[31];
cx q[100], q[39];
cx q[78], q[43];
cx q[69], q[49];
cx q[92], q[96];
cx q[76], q[87];
cx q[58], q[32];
cx q[89], q[1];
cx q[46], q[5];
cx q[67], q[7];
cx q[68], q[8];
cx q[77], q[15];
cx q[107], q[98];
cx q[33], q[17];
cx q[45], q[20];
cx q[63], q[27];
cx q[47], q[34];
cx q[61], q[35];
cx q[60], q[6];
cx q[62], q[51];
cx q[102], q[105];
cx q[42], q[94];
cx q[70], q[11];
cx q[82], q[24];
cx q[59], q[37];
cx q[81], q[44];
cx q[95], q[54];
cx q[76], q[72];
cx q[99], q[13];
cx q[32], q[85];
cx q[58], q[16];
cx q[100], q[19];
cx q[87], q[21];
cx q[9], q[22];
cx q[101], q[28];
cx q[92], q[30];
cx q[0], q[31];
cx q[2], q[39];
cx q[83], q[49];
cx q[96], q[64];
cx q[78], q[80];
cx q[73], q[66];
cx q[69], q[106];
cx q[79], q[50];
cx q[48], q[88];
cx q[91], q[89];
cx q[41], q[1];
cx q[90], q[5];
cx q[67], q[6];
cx q[61], q[10];
cx q[68], q[15];
cx q[97], q[18];
cx q[65], q[20];
cx q[107], q[26];
cx q[63], q[43];
cx q[51], q[56];
cx q[86], q[77];
cx q[74], q[7];
cx q[60], q[46];
cx q[81], q[29];
cx q[82], q[40];
cx q[59], q[55];
cx q[95], q[70];
cx q[52], q[83];
cx q[71], q[72];
cx q[58], q[98];
cx q[94], q[16];
cx q[69], q[17];
cx q[99], q[21];
cx q[105], q[22];
cx q[66], q[23];
cx q[2], q[25];
cx q[87], q[27];
cx q[96], q[28];
cx q[101], q[30];
cx q[76], q[31];
cx q[48], q[35];
cx q[79], q[36];
cx q[0], q[38];
cx q[9], q[39];
cx q[47], q[49];
cx q[73], q[64];
cx q[33], q[80];
cx q[32], q[45];
cx q[50], q[100];
cx q[62], q[106];
cx q[42], q[78];
cx q[88], q[102];
cx q[103], q[7];
cx q[89], q[14];
cx q[46], q[15];
cx q[61], q[18];
cx q[68], q[19];
cx q[90], q[20];
cx q[63], q[37];
cx q[91], q[53];
cx q[51], q[57];
cx q[60], q[12];
cx q[82], q[11];
cx q[93], q[85];
cx q[59], q[13];
cx q[66], q[10];
cx q[106], q[98];
cx q[41], q[16];
cx q[77], q[22];
cx q[102], q[23];
cx q[69], q[24];
cx q[99], q[26];
cx q[105], q[27];
cx q[107], q[30];
cx q[94], q[31];
cx q[45], q[34];
cx q[0], q[35];
cx q[96], q[36];
cx q[48], q[38];
cx q[101], q[43];
cx q[9], q[44];
cx q[42], q[49];
cx q[47], q[54];
cx q[86], q[64];
cx q[72], q[80];
cx q[83], q[84];
cx q[79], q[100];
cx q[88], q[67];
cx q[73], q[78];
cx q[32], q[62];
cx q[33], q[87];
cx q[58], q[92];
cx q[65], q[76];
cx q[2], q[50];
cx q[63], q[52];
cx q[104], q[14];
cx q[95], q[19];
cx q[74], q[25];
cx q[46], q[28];
cx q[75], q[85];
cx q[96], q[8];
cx q[92], q[15];
cx q[83], q[98];
cx q[51], q[16];
cx q[77], q[17];
cx q[88], q[18];
cx q[106], q[20];
cx q[72], q[22];
cx q[78], q[24];
cx q[90], q[26];
cx q[62], q[27];
cx q[91], q[30];
cx q[105], q[31];
cx q[107], q[34];
cx q[101], q[35];
cx q[42], q[36];
cx q[45], q[37];
cx q[99], q[38];
cx q[73], q[39];
cx q[47], q[40];
cx q[48], q[43];
cx q[60], q[44];
cx q[79], q[49];
cx q[41], q[53];
cx q[2], q[54];
cx q[102], q[55];
cx q[33], q[56];
cx q[65], q[57];
cx q[32], q[64];
cx q[9], q[80];
cx q[0], q[84];
cx q[50], q[68];
cx q[87], q[89];
cx q[69], q[66];
cx q[94], q[81];
cx q[86], q[6];
cx q[58], q[4];
cx q[61], q[67];
cx q[100], q[70];
cx q[103], q[76];
cx q[97], q[19];
cx q[82], q[25];
cx q[51], q[6];
cx q[59], q[16];
cx q[63], q[18];
cx q[90], q[21];
cx q[65], q[22];
cx q[77], q[23];
cx q[88], q[24];
cx q[106], q[26];
cx q[60], q[27];
cx q[102], q[29];
cx q[62], q[35];
cx q[68], q[36];
cx q[94], q[37];
cx q[104], q[39];
cx q[45], q[40];
cx q[100], q[43];
cx q[46], q[44];
cx q[99], q[49];
cx q[48], q[53];
cx q[93], q[54];
cx q[81], q[55];
cx q[107], q[56];
cx q[2], q[57];
cx q[61], q[64];
cx q[58], q[80];
cx q[92], q[101];
cx q[9], q[95];
cx q[0], q[89];
cx q[103], q[50];
cx q[73], q[67];
cx q[33], q[41];
cx q[66], q[78];
cx q[69], q[32];
cx q[74], q[72];
cx q[47], q[86];
cx q[91], q[87];
cx q[105], q[76];
cx q[83], q[42];
cx q[70], q[79];
cx q[96], q[15];
cx q[52], q[22];
cx q[63], q[24];
cx q[60], q[25];
cx q[90], q[27];
cx q[77], q[28];
cx q[104], q[31];
cx q[91], q[34];
cx q[78], q[35];
cx q[68], q[37];
cx q[105], q[38];
cx q[101], q[39];
cx q[106], q[43];
cx q[89], q[44];
cx q[41], q[49];
cx q[0], q[53];
cx q[100], q[54];
cx q[107], q[57];
cx q[97], q[64];
cx q[88], q[80];
cx q[2], q[84];
cx q[50], q[62];
cx q[33], q[58];
cx q[86], q[93];
cx q[51], q[67];
cx q[74], q[82];
cx q[70], q[103];
cx q[32], q[102];
cx q[96], q[72];
cx q[94], q[9];
cx q[65], q[69];
cx q[81], q[59];
cx q[87], q[61];
cx q[46], q[92];
cx q[76], q[79];
cx q[95], q[83];
cx q[66], q[73];
cx q[99], q[48];
cx q[42], q[47];
cx q[45], q[10];
cx q[89], q[13];
cx q[93], q[98];
cx q[52], q[21];
cx q[75], q[22];
cx q[67], q[31];
cx q[69], q[34];
cx q[103], q[37];
cx q[60], q[38];
cx q[77], q[40];
cx q[81], q[44];
cx q[45], q[49];
cx q[105], q[53];
cx q[50], q[54];
cx q[102], q[64];
cx q[106], q[80];
cx q[90], q[84];
cx q[63], q[41];
cx q[92], q[74];
cx q[99], q[33];
cx q[51], q[107];
cx q[79], q[47];
cx q[101], q[48];
cx q[68], q[95];
cx q[78], q[100];
cx q[59], q[32];
cx q[82], q[12];
cx q[61], q[14];
cx q[66], q[72];
cx q[76], q[94];
cx q[62], q[91];
cx q[58], q[87];
cx q[73], q[86];
cx q[65], q[2];
cx q[97], q[96];
cx q[70], q[83];
cx q[0], q[9];
cx q[104], q[88];
cx q[46], q[42];
cx q[88], q[31];
cx q[106], q[44];
cx q[61], q[53];
cx q[77], q[54];
cx q[45], q[55];
cx q[48], q[56];
cx q[9], q[57];
cx q[72], q[64];
cx q[33], q[80];
cx q[59], q[84];
cx q[100], q[68];
cx q[101], q[78];
cx q[105], q[66];
cx q[90], q[89];
cx q[107], q[67];
cx q[82], q[96];
cx q[102], q[69];
cx q[63], q[91];
cx q[99], q[32];
cx q[95], q[73];
cx q[103], q[79];
cx q[104], q[76];
cx q[86], q[2];
cx q[47], q[83];
cx q[75], q[74];
cx q[60], q[97];
cx q[52], q[50];
cx q[87], q[65];
cx q[93], q[92];
cx q[51], q[58];
cx q[42], q[0];
cx q[94], q[62];
cx q[81], q[70];
cx q[41], q[46];
cx q[88], q[40];
cx q[45], q[64];
cx q[48], q[80];
cx q[9], q[84];
cx q[69], q[97];
cx q[83], q[93];
cx q[62], q[32];
cx q[77], q[75];
cx q[61], q[33];
cx q[78], q[67];
cx q[66], q[2];
cx q[68], q[103];
cx q[102], q[79];
cx q[58], q[60];
cx q[96], q[95];
cx q[107], q[87];
cx q[52], q[51];
cx q[91], q[0];
cx q[59], q[47];
cx q[74], q[76];
cx q[101], q[104];
cx q[100], q[105];
cx q[90], q[46];
cx q[72], q[73];
cx q[82], q[81];
cx q[86], q[50];
cx q[89], q[65];
cx q[106], q[42];
cx q[99], q[70];
cx q[63], q[41];
cx q[92], q[94];
