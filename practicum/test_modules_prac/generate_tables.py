import randop


def build_random_test_tables(self, LOG, query_count):
    queries = []
    data = []
    for rowkey in range(query_count):
        name = randop.create_random_string(10)
        age = randop.create_random_int(1, 10)
        address = randop.create_random_string(10)
        query = 'INSERT INTO CORP (ID,NAME,AGE,ADDRESS) VALUES (%s, %s, %s, %s);'
        data.append((rowkey, name, age, address))
        queries.append(query)
    try:
        for db in self.dbs:
            conn = self.__dict__[db]
            cur = conn.cursor()
            cur.execute("""CREATE TABLE CORP(ID INT, NAME VARCHAR(20), AGE INT, ADDRESS VARCHAR(20))""")
            for i in range(len(queries)):
                cur.execute(queries[i], data[i])
            conn.commit()
            LOG.info("table/batch passed {}".format(db))
        # The name of the table created is CORP
        self.table_names = ["CORP"]
    except:
        LOG.error("table/batch failed {}".format(db))
