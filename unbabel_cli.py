import sys
import heapq
import argparse

class CustomParser(argparse.ArgumentParser):
    """Class to show the help message when there is an error when parsing the
        arguments
    """
    def error(self, message):
        """Method called when some error occurs during the argument parsing

        Arguments:
            message {string} -- the message explaining the error
        """
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)


if __name__ == "__main__":
    parser = CustomParser(description='Outputs the moving average '+
                                        'of the input file minute by minute.')
    parser.add_argument('--input-file', required=True,
                    help='the file to be parsed')
    parser.add_argument('--window-size', type=int, default=10,
                    help='the window size, in minutes, that will be averaged')

    args = parser.parse_args()
    print(args.accumulate(args.integers))
