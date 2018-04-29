#
# Simson's growing SQL class. Generally, this is easier than using an ORM, if you are comfortable with SQL
# 
import datetime

class SLGSQL:
    def iso_now():
        """Report current time in ISO-8601 format"""
        return datetime.datetime.now().isoformat()[0:19]

    def create_schema(conn,schema):
        """Create the schema if it doesn't exist."""
        c = conn.cursor()
        for line in schema.split(";"):
            c.execute(line)

    def execselect(conn, sql, vals=()):
        """Execute a SQL query and return the first line"""
        c = conn.cursor()
        c.execute(sql, vals)
        return c.fetchone()

