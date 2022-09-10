import sys

def parse_cli(cli_args) -> list:
    '''
    parse cli args
    '''
    if len(cli_args) < 2:
        print("One Argument Required, [Input Filename, Opt. Output Filename]")
        print("\t Received:", cli_args)
    else:
        print("\t Received:", cli_args)
        in_filename = cli_args[1]
        out_filename = "data/output"
        if len(cli_args) > 2:
            out_filename = cli_args[2]
    return in_filename, out_filename


def main(cli_args: list) -> None:
    '''
    main function
    '''
    in_filename, out_filename = parse_cli(cli_args)
    print("in_filename:", in_filename)
    print("out_filename:", out_filename)
    with open(in_filename, "r", encoding="utf8") as in_file:
        lines = in_file.readlines()
    with open(out_filename, "w", encoding="utf8") as out_file:
        for line in lines:
            if "data[" in line:
                value = line.split(":").pop()
                value = value.split("\\")[0]
                print("result:", str(value))
                out_file.write(value + "\n")


if __name__ == "__main__":
    main(sys.argv)
