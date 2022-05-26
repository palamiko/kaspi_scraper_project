from db_worker.db_engine import get_price_history_item, create_record_price


def main():
    a = [(3, 45000, '2022-05-25 19:38:56.061000'), (1, 76000, '2022-05-26 19:38:56.061000'), (3, 50000, '2022-05-26 19:38:56.061000') ]
    create_record_price(a)


if __name__ == '__main__':
    main()
