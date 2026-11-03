from database.connection import get_connection


def insert_investor_data(data):
    """
    Insert extracted financial information into PostgreSQL.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        query = """
        INSERT INTO investor_data (
            company,
            year,
            revenue,
            net_income,
            operating_income,
            operating_cash_flow,
            total_assets,
            total_liabilities,
            risk_factors,
            growth_drivers
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (company, year)
        DO UPDATE SET
            revenue = EXCLUDED.revenue,
            net_income = EXCLUDED.net_income,
            operating_income = EXCLUDED.operating_income,
            operating_cash_flow = EXCLUDED.operating_cash_flow,
            total_assets = EXCLUDED.total_assets,
            total_liabilities = EXCLUDED.total_liabilities,
            risk_factors = EXCLUDED.risk_factors,
            growth_drivers = EXCLUDED.growth_drivers;
        """

        cursor.execute(
            query,
            (
                data.company,
                int(data.fiscal_year)
                if data.fiscal_year
                else None,

                data.revenue,
                data.net_income,
                data.operating_income,
                data.operating_cash_flow,
                data.total_assets,
                data.total_liabilities,

                "\n".join(data.risk_factors)
                if data.risk_factors
                else None,

                "\n".join(data.growth_drivers)
                if data.growth_drivers
                else None,
            )
        )

        connection.commit()

        print(
            "Financial data inserted into PostgreSQL successfully."
        )

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()