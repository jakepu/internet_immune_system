from components.dummy_parser import DummyParser
from components.synchronizer import Synchronizer


def main():
    parser1 = DummyParser('src_a')
    parser2 = DummyParser('src_b')
    parser3 = DummyParser('src_c')

    parsers = [parser1, parser2, parser3]

    synchronizer = Synchronizer(parsers)

    while range(1, 10):
        data = synchronizer.get_next_most_recent()
        print('Synchronizer: most recent timestamp is ' + str(data.timestamp))


if __name__ == "__main__":
    main()

