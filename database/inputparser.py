# CREATE table_name (column_name [INDEXED] [, ...]);
# INSERT [INTO] table_name (“value” [, ...]);
# SELECT FROM table_name


class InputParser:

    def to_single_line(row_data):
        res = ''
        if(isinstance(list, row_data)):
            for row in row_data:
                res += row.split()
        return res


    def parse_input(data):
        data = InputParser.to_single_line(data)
        # Need Tex-Yacc realisation