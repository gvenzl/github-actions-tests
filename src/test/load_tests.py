import os
import oracledb as o
import unittest


class TestDBLayer(unittest.TestCase):

    APP_USER = ""
    APP_USER_PWD = ""
    DB_HOST = ""
    DB_NAME = ""

    conn = None

    def get_conn(self):
        if self.conn is None:
            self.conn = o.connect(
                            user=self.APP_USER,
                            password=self.APP_USER_PWD,
                            dsn=self.DB_HOST+"/"+self.DB_NAME
            )
        return self.conn

    def test_create_table(self):
        print("TEST CREATE TABLE...")
        print()
        with self.get_conn() as conn:
            with conn.cursor() as c:
                print("Create table")
                c.execute("CREATE TABLE foo (id NUMBER)")

                print("Check table exists")
                c.execute("SELECT COUNT(1) FROM foo")
                self.assertEqual(c.fetchone()[0], 0)

                print("Drop table")
                c.execute("DROP TABLE foo")
        print()

    def test_select_data(self):
        print("TEST SELECT data")
        rows = 10
        with self.get_conn() as conn:
            with conn.cursor() as c:
                print("Create table")
                c.execute("CREATE TABLE test (id NUMBER)")

                print("Load data into table...")
                for i in range(0, rows):
                    c.execute("INSERT INTO test (id) VALUES (:id)", (i,))
                    print("Row loaded.")

                print("Verify load.")
                c.execute("SELECT COUNT(1) FROM test")
                self.assertEqual(c.fetchone()[0], rows)


if __name__ == "__main__":
    TestDBLayer.APP_USER = os.getenv("APP_USER")
    TestDBLayer.APP_USER_PWD = os.getenv("APP_USER_PWD")
    TestDBLayer.DB_HOST = os.getenv("DB_HOST", "localhost")
    TestDBLayer.DB_NAME = os.getenv("DB_NAME")
    unittest.main()
