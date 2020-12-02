// File: CNN_Controler.v
// Generated by MyHDL 0.11
// Date: Tue Dec  1 19:53:06 2020


`timescale 1ns/10ps

module CNN_Controler (
    clk_i,
    fill_req,
    out_valid,
    data_i,
    data_o
);


input clk_i;
output fill_req;
reg fill_req;
output out_valid;
reg out_valid;
input [15:0] data_i;
output [15:0] data_o;
reg [15:0] data_o;

reg [15:0] bus3;
reg [15:0] add_b;
reg [2:0] state;
reg [1:0] fil_col_cnt;
reg [15:0] input_ram_data_out;
reg result_out;
reg sum_is_zero;
reg [9:0] buff;
reg [15:0] bus11;
reg [2:0] in_col_cnt;
reg [1:0] in_row_cnt;
reg [15:0] mult_a;
reg [15:0] bus10;
reg finished;
reg [15:0] bus7;
reg [15:0] bus9;
reg filter_ram_wr;
wire [1:0] output_ram_col;
wire [15:0] input_ram_data_in;
reg [0:0] out_row_cnt;
reg [15:0] bus0;
reg [15:0] output_ram_data_out;
wire [15:0] output_ram_data_in;
reg filter_ram_en;
wire [15:0] add_out;
wire [1:0] input_ram_row;
reg sum_ready;
reg [9:0] mat_cnt;
reg [15:0] bus6;
reg [15:0] mult_b;
reg [1:0] reset_cnt;
wire [1:0] filter_ram_row;
reg [15:0] bus8;
wire [15:0] mult_out;
reg [15:0] buffer;
reg output_ram_wr;
reg [15:0] bus1;
reg [15:0] add_a;
reg input_ram_en;
reg [15:0] bus2;
wire [1:0] filter_ram_col;
reg [1:0] fil_row_cnt;
reg [15:0] bus4;
reg [15:0] bus5;
reg [3:0] acc_cnt;
reg [1:0] out_col_cnt;
reg [15:0] sum;
reg input_ram_wr;
wire [15:0] filter_ram_data_in;
reg output_ram_en;
reg mult_is_zero;
wire [0:0] output_ram_row;
wire [2:0] input_ram_col;
reg [15:0] filter_ram_data_out;
wire [2:0] chunk_insts_3_addr;
wire [3:0] chunk_insts_0_addr;
wire [4:0] chunk_insts_1_addr;
wire [31:0] chunk_insts_2_multer_out;
reg [15:0] chunk_insts_3_mem [0:8-1];
reg [15:0] chunk_insts_0_mem [0:16-1];
reg [15:0] chunk_insts_1_mem [0:32-1];




assign chunk_insts_0_addr = ((filter_ram_row * 3) + filter_ram_col);


always @(posedge clk_i) begin: CNN_CONTROLER_LOC_INSTS_CHUNK_INSTS_0_LOC_INSTS_CHUNK_INSTS_K
    if (filter_ram_en) begin
        if (filter_ram_wr) begin
            chunk_insts_0_mem[chunk_insts_0_addr] <= filter_ram_data_in;
        end
        else begin
            filter_ram_data_out <= chunk_insts_0_mem[chunk_insts_0_addr];
        end
    end
end



assign chunk_insts_1_addr = ((input_ram_row * 6) + input_ram_col);


always @(posedge clk_i) begin: CNN_CONTROLER_LOC_INSTS_CHUNK_INSTS_1_LOC_INSTS_CHUNK_INSTS_K
    if (input_ram_en) begin
        if (input_ram_wr) begin
            chunk_insts_1_mem[chunk_insts_1_addr] <= input_ram_data_in;
        end
        else begin
            input_ram_data_out <= chunk_insts_1_mem[chunk_insts_1_addr];
        end
    end
end



assign chunk_insts_2_multer_out = (mult_a * mult_b);



assign mult_out = chunk_insts_2_multer_out[25-1:9];



assign chunk_insts_3_addr = ((output_ram_row * 4) + output_ram_col);


always @(posedge clk_i) begin: CNN_CONTROLER_LOC_INSTS_CHUNK_INSTS_3_LOC_INSTS_CHUNK_INSTS_K
    if (output_ram_en) begin
        if (output_ram_wr) begin
            chunk_insts_3_mem[chunk_insts_3_addr] <= output_ram_data_in;
        end
        else begin
            output_ram_data_out <= chunk_insts_3_mem[chunk_insts_3_addr];
        end
    end
end



assign add_out = (add_a + add_b);



assign output_ram_col = out_col_cnt;
assign output_ram_row = out_row_cnt;
assign output_ram_data_in = sum;



assign filter_ram_col = fil_col_cnt;
assign filter_ram_row = fil_row_cnt;
assign filter_ram_data_in = buffer;


always @(output_ram_data_out, result_out) begin: CNN_CONTROLER_LOC_INSTS_CHUNK_INSTS_7_C
    if (result_out) begin
        data_o = output_ram_data_out;
    end
    else begin
        data_o = 0;
    end
end


always @(sum_is_zero, add_out) begin: CNN_CONTROLER_LOC_INSTS_CHUNK_INSTS_8_C
    if ((sum_is_zero == 1)) begin
        sum = 0;
    end
    else begin
        sum = add_out;
    end
end



assign input_ram_col = in_col_cnt;
assign input_ram_row = in_row_cnt;
assign input_ram_data_in = data_i;


always @(input_ram_data_out, mult_is_zero, filter_ram_data_out) begin: CNN_CONTROLER_LOC_INSTS_CHUNK_INSTS_10_C
    if (mult_is_zero) begin
        mult_a = 0;
        mult_b = 0;
    end
    else begin
        mult_a = input_ram_data_out;
        mult_b = filter_ram_data_out;
    end
end


always @(posedge clk_i) begin: CNN_CONTROLER_LOC_INSTS_CHUNK_INSTS_K
    if (($signed({1'b0, reset_cnt}) < (4 - 1))) begin
        in_row_cnt <= 0;
        in_col_cnt <= 0;
        fil_row_cnt <= 0;
        fill_req <= 0;
        fil_col_cnt <= 0;
        bus0 <= 51;
        bus1 <= 102;
        bus2 <= 204;
        bus3 <= 102;
        bus4 <= 0;
        bus5 <= 153;
        bus6 <= 102;
        bus7 <= 256;
        bus8 <= 51;
        bus9 <= 0;
        bus10 <= 0;
        bus11 <= 0;
        buffer <= 0;
        out_row_cnt <= 0;
        out_col_cnt <= 0;
        mat_cnt <= 0;
        acc_cnt <= 0;
        out_valid <= 0;
        result_out <= 0;
        finished <= 0;
        sum_is_zero <= 0;
        buff <= 0;
        sum_ready <= 0;
        reset_cnt <= (reset_cnt + 1);
        if (($signed({1'b0, reset_cnt}) == (4 - 1))) begin
            input_ram_en <= 1;
            input_ram_wr <= 1;
            fill_req <= 1;
            state <= 3'b000;
        end
        else if (($signed({1'b0, reset_cnt}) == (4 - 2))) begin
            fill_req <= 1;
        end
    end
    else if ((state == 3'b000)) begin
        input_ram_en <= 1;
        input_ram_wr <= 1;
        fill_req <= 1;
        if (($signed({1'b0, in_col_cnt}) == (6 - 1))) begin
            in_row_cnt <= (in_row_cnt + 1);
            in_col_cnt <= 0;
        end
        else begin
            in_col_cnt <= (in_col_cnt + 1);
        end
        if ((($signed({1'b0, in_row_cnt}) == (4 - 1)) && ($signed({1'b0, in_col_cnt}) == (6 - 1)))) begin
            filter_ram_en <= 1;
            filter_ram_wr <= 1;
            case (mat_cnt)
                'h0: begin
                    buffer <= bus0;
                end
                'h1: begin
                    buffer <= bus1;
                end
                'h2: begin
                    buffer <= bus2;
                end
                'h3: begin
                    buffer <= bus3;
                end
                'h4: begin
                    buffer <= bus4;
                end
                'h5: begin
                    buffer <= bus5;
                end
                'h6: begin
                    buffer <= bus6;
                end
                'h7: begin
                    buffer <= bus7;
                end
                'h8: begin
                    buffer <= bus8;
                end
                'h9: begin
                    buffer <= bus9;
                end
                'ha: begin
                    buffer <= bus10;
                end
                'hb: begin
                    buffer <= bus11;
                end
                default: begin
                    buffer <= 0;
                end
            endcase
            mat_cnt <= (mat_cnt + 1);
            fill_req <= 0;
            state <= 3'b001;
        end
        else if ((($signed({1'b0, in_row_cnt}) == (4 - 1)) && ($signed({1'b0, in_col_cnt}) == (6 - 2)))) begin
            fill_req <= 0;
        end
    end
    else if ((state == 3'b001)) begin
        if (((fil_col_cnt == 0) && (fil_row_cnt == 0))) begin
            input_ram_en <= 0;
            input_ram_wr <= 0;
            in_row_cnt <= 0;
            in_col_cnt <= 0;
        end
        if (($signed({1'b0, fil_col_cnt}) == (3 - 1))) begin
            fil_row_cnt <= (fil_row_cnt + 1);
            fil_col_cnt <= 0;
        end
        else begin
            fil_col_cnt <= (fil_col_cnt + 1);
        end
        mat_cnt <= (mat_cnt + 1);
        case (mat_cnt)
            'h0: begin
                buffer <= bus0;
            end
            'h1: begin
                buffer <= bus1;
            end
            'h2: begin
                buffer <= bus2;
            end
            'h3: begin
                buffer <= bus3;
            end
            'h4: begin
                buffer <= bus4;
            end
            'h5: begin
                buffer <= bus5;
            end
            'h6: begin
                buffer <= bus6;
            end
            'h7: begin
                buffer <= bus7;
            end
            'h8: begin
                buffer <= bus8;
            end
            'h9: begin
                buffer <= bus9;
            end
            'ha: begin
                buffer <= bus10;
            end
            'hb: begin
                buffer <= bus11;
            end
            default: begin
                buffer <= 0;
            end
        endcase
        filter_ram_en <= 1;
        filter_ram_wr <= 1;
        if ((($signed({1'b0, fil_row_cnt}) == (3 - 1)) && ($signed({1'b0, fil_col_cnt}) == (3 - 1)))) begin
            buff <= 4;
            fil_row_cnt <= 0;
            fil_col_cnt <= 0;
            in_col_cnt <= 0;
            in_row_cnt <= 0;
            input_ram_en <= 1;
            input_ram_wr <= 0;
            filter_ram_en <= 1;
            filter_ram_wr <= 0;
            add_a <= sum;
            add_b <= mult_out;
            sum_is_zero <= 1;
            mult_is_zero <= 1;
            state <= 3'b010;
        end
    end
    else if ((state == 3'b010)) begin
        if ((buff == 4)) begin
            buff <= 3;
            in_col_cnt <= 0;
            in_row_cnt <= 0;
            input_ram_en <= 1;
            input_ram_wr <= 0;
            filter_ram_en <= 1;
            filter_ram_wr <= 0;
            add_a <= sum;
            add_b <= mult_out;
            out_col_cnt <= 0;
            out_row_cnt <= 0;
            sum_is_zero <= 0;
            mult_is_zero <= 1;
            fil_row_cnt <= 0;
            fil_col_cnt <= 0;
            buff <= 5;
        end
        else if ((buff < 3)) begin
            buff <= (buff + 1);
            in_col_cnt <= out_col_cnt;
            in_row_cnt <= out_row_cnt;
            add_a <= sum;
            add_b <= mult_out;
            sum_is_zero <= 1;
        end
        else if ((buff == 6)) begin
            sum_is_zero <= 1;
            output_ram_en <= 1;
            output_ram_wr <= 0;
            add_a <= sum;
            add_b <= mult_out;
            buff <= 8;
            sum_ready <= 0;
            mult_is_zero <= 1;
        end
        else if ((buff == 7)) begin
            sum_is_zero <= 0;
            output_ram_en <= 1;
            output_ram_wr <= 0;
            add_a <= sum;
            add_b <= mult_out;
            buff <= 6;
            sum_ready <= 0;
            mult_is_zero <= 1;
        end
        else if ((buff == 8)) begin
            add_a <= sum;
            add_b <= mult_out;
            if (($signed({1'b0, out_col_cnt}) == (4 - 1))) begin
                out_row_cnt <= (out_row_cnt + 1);
                out_col_cnt <= 0;
                buff <= 7;
            end
            else begin
                out_col_cnt <= (out_col_cnt + 1);
                buff <= 7;
            end
            sum_is_zero <= 1;
            mult_is_zero <= 1;
            buff <= 5;
        end
        else begin
            if (((fil_col_cnt == 0) && (fil_row_cnt == 3))) begin
                fil_row_cnt <= 0;
                fil_col_cnt <= 0;
                if (($signed({1'b0, out_col_cnt}) == (4 - 1))) begin
                    in_col_cnt <= 0;
                    in_row_cnt <= (out_row_cnt + 1);
                end
                else begin
                    in_col_cnt <= (out_col_cnt + 1);
                    in_row_cnt <= out_row_cnt;
                end
                buff <= 7;
                sum_is_zero <= 1;
            end
            else if (($signed({1'b0, fil_col_cnt}) == (3 - 1))) begin
                fil_row_cnt <= (fil_row_cnt + 1);
                fil_col_cnt <= 0;
                in_col_cnt <= out_col_cnt;
                in_row_cnt <= ((out_row_cnt + fil_row_cnt) + 1);
            end
            else begin
                fil_col_cnt <= (fil_col_cnt + 1);
                in_col_cnt <= ((out_col_cnt + fil_col_cnt) + 1);
            end
            sum_is_zero <= 0;
            mult_is_zero <= 0;
            sum_ready <= 0;
            input_ram_en <= 1;
            input_ram_wr <= 0;
            filter_ram_en <= 1;
            filter_ram_wr <= 0;
            add_a <= sum;
            add_b <= mult_out;
            if (((fil_col_cnt == 0) && (fil_row_cnt == 3))) begin
                if ((($signed({1'b0, out_row_cnt}) == (2 - 1)) && ($signed({1'b0, out_col_cnt}) == (4 - 1)))) begin
                    state <= 3'b011;
                    buff <= 0;
                end
                sum_ready <= 1;
                output_ram_en <= 1;
                output_ram_wr <= 1;
                mult_is_zero <= 1;
                sum_is_zero <= 0;
            end
        end
    end
    else if ((state == 3'b011)) begin
        if ((buff == 0)) begin
            sum_is_zero <= 1;
            out_row_cnt <= 0;
            out_col_cnt <= 0;
            output_ram_en <= 1;
            output_ram_wr <= 0;
            add_a <= sum;
            add_b <= mult_out;
            buff <= 6;
            sum_ready <= 0;
            mult_is_zero <= 1;
            buff <= 1;
        end
        if ((buff == 1)) begin
            output_ram_en <= 1;
            output_ram_wr <= 0;
            state <= 3'b100;
        end
    end
    else if ((state == 3'b100)) begin
        acc_cnt <= (acc_cnt + 1);
        out_valid <= 1;
        if (($signed({1'b0, out_col_cnt}) == (4 - 1))) begin
            out_row_cnt <= (out_row_cnt + 1);
            out_col_cnt <= 0;
        end
        else begin
            out_col_cnt <= (out_col_cnt + 1);
        end
        result_out <= 1;
        output_ram_en <= 1;
        output_ram_wr <= 0;
        if ((acc_cnt == (2 * 4))) begin
            reset_cnt <= 0;
            result_out <= 0;
            state <= 3'b101;
        end
    end
    else if ((state == 3'b101)) begin
        sum_is_zero <= 1;
        mult_is_zero <= 1;
        out_valid <= 0;
        input_ram_en <= 0;
        input_ram_wr <= 0;
        filter_ram_en <= 0;
        filter_ram_wr <= 0;
    end
    else begin
        state <= 3'b100;
    end
end

endmodule
