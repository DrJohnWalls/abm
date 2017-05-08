"""In this file, we provide functions for creating and updating the database"""

import sqlite3
import stockmarket.parameters as par

conn = sqlite3.connect(par.database_name)
cur = conn.cursor()


def create_tables():
    cur.executescript('''
    DROP TABLE IF EXISTS Transactions;
    DROP TABLE IF EXISTS Statevariables;
    DROP TABLE IF EXISTS Variabletypes;
    DROP TABLE IF EXISTS Objects;
    DROP TABLE IF EXISTS Experiments;
    DROP TABLE IF EXISTS Transactors;

    CREATE TABLE Transactions (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        experiment_id INTEGER,
        seed INTEGER,
        period INTEGER,
        amount_of_product REAL,
        amount_of_money REAL
    );

    CREATE TABLE Transactors(
        transaction_id INTEGER NOT NULL,
		transactor_id INTEGER NOT NULL,
		role REAL,
		PRIMARY KEY (transaction_id, transactor_id)
    );

    CREATE TABLE Statevariables (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        experiment_id INTEGER,
        seed INTEGER,
        period INTEGER,
        variable_id INTEGER,
        owner_id INTEGER,
        value REAL
    );

    CREATE TABLE Variabletypes (
        id  INTEGER NOT NULL PRIMARY KEY
            AUTOINCREMENT UNIQUE,
        variable_type TEXT  UNIQUE
    );

    CREATE TABLE Objects (
        id  INTEGER NOT NULL PRIMARY KEY
            AUTOINCREMENT UNIQUE,
        object_name TEXT  UNIQUE,
        object_type TEXT
    );

    CREATE TABLE Experiments (
        id  INTEGER NOT NULL PRIMARY KEY
            AUTOINCREMENT UNIQUE,
        experiment TEXT  UNIQUE,
        parameter_space TEXT
    );

    ''')


def record_statevariables(period, agent):
    """Records all state variables for this agent in the Statevariable and related tables"""
    variables = vars(agent)
    for variable in variables:
        # store the variable type into the variabletypes table
        cur.execute("INSERT OR IGNORE INTO Variabletypes (variable_type) VALUES (?)", (str(variable), ))
        cur.execute("SELECT id FROM Variabletypes WHERE variable_type = ?", (str(variable),))
        variable_type_id = cur.fetchone()[0]

        # store the agent and type of agent in the objects table
        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)", (repr(agent), repr(agent)[:repr(agent).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(agent),))
        owner_id = cur.fetchone()[0]

        cur.execute("INSERT INTO Statevariables (experiment_id, seed, period, "
                    "variable_id, owner_id, value) VALUES (?,?,?,?,?,?)",
                    (par.experiment_id, par.seed, period, variable_type_id, owner_id, str(variables[variable])))


def record_transaction(buyer, seller, stock, amount_of_product, amount_of_money, quarter):
    cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                (repr(buyer), repr(buyer)[:repr(buyer).find('_')]))
    cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(buyer),))
    buyer_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                (repr(seller), repr(seller)[:repr(seller).find('_')]))
    cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(seller),))
    seller_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                (repr(stock), repr(stock)[:repr(stock).find('_')]))
    cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(stock),))
    stock_id = cur.fetchone()[0]

    cur.execute("INSERT INTO Transactions (experiment_id, seed, period, amount_of_product, "
                "amount_of_money) VALUES (?,?,?,?,?)",
                (par.experiment_id, par.seed, quarter,
                 amount_of_product, amount_of_money))
    cur.execute("SELECT MAX(id) FROM Transactions")
    transaction_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                (transaction_id, buyer_id, 'buyer'))
    cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                (transaction_id, seller_id, 'seller'))
    cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                (transaction_id, stock_id, 'stock'))


def commit():
    conn.commit()


def close():
    cur.close()
