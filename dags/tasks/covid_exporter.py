
def run(datadate):
    import csv
    import psycopg
    from airflow.hooks.base_hook import BaseHook
    from airflow.models import Variable

    greeting = Variable.get("GREETING")
    print(f"Got variable, greeting: {greeting}")
    def export_to_postgres(data):
        conn_info = BaseHook.get_connection("job_postgres")
        with psycopg.connect(f"host={conn_info.host} dbname=dataset "
                             + f"user={conn_info.login} password={conn_info.password}") as conn:
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO covid values(%s, %s, %s, %s)", data)
            conn.commit()

    data = []
    with open(f"/shared_dir/covid-{datadate}.csv", "r") as f:
        csv_data = csv.reader(f, delimiter=',')
        got_header = False
        for row in csv_data:
            if not got_header:
                got_header = True
                continue
            data.append((row[3], row[7], row[8], row[4][0:10]))
    export_to_postgres(data)

