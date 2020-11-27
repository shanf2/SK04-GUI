import sqlite3 as sq

con = sq.connect('Users.db')
c = con.cursor()

c.execute("DROP TABLE Userlist")
c.execute("DROP TABLE Params")

userlist_sql = """
CREATE TABLE Userlist (
    username text NOT NULL,
    password text NOT NULL)
"""
c.execute(userlist_sql)

params_sql = """
CREATE TABLE Parameters (
    id integer PRIMARY KEY,
    mode integer NOT NULL,
    lrl integer NOT NULL,
    url integer NOT NULL,
    a_amp integer NOT NULL,
    v_amp integer NOT NULL,
    pw integer NOT NULL,
    a_sensi integer NOT NULL,
    v_sensi integer NOT NULL,
    rp integer NOT NULL,
    av_delay integer NOT NULL,
    msr integer NOT NULL,
    act_thresh integer NOT NULL,
    react_t integer NOT NULL,
    res_fact integer NOT NULL,
    rec_t integer NOT NULL,
    uid integer NOT NULL,
    FOREIGN KEY (uid) REFERENCES Userlist (oid))
    """
c.execute(params_sql)