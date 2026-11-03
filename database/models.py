from database.connection import get_connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS investor_data (

            id SERIAL PRIMARY KEY,

            company TEXT NOT NULL,

            year INTEGER NOT NULL,

            revenue TEXT,

            net_income TEXT,

            operating_income TEXT,

            operating_cash_flow TEXT,

            total_assets TEXT,

            total_liabilities TEXT,

            risk_factors TEXT,

            growth_drivers TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(company, year)
        );
        """
    )

    connection.commit()

    cursor.close()

    connection.close()

    print("Investor database table created successfully.")


if __name__ == "__main__":

    create_tables()