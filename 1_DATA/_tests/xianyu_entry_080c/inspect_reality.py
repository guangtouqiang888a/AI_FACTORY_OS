import sqlite3, os
con = sqlite3.connect(r"file:D:/AI_FACTORY_OS/data/ai_factory.db?mode=ro", uri=True)
con.row_factory = sqlite3.Row
c = con.cursor()

def cnt(q):
    return c.execute(q).fetchone()[0]

print("obs", cnt("select count(*) from market_observations"))
print("real", cnt("select count(*) from market_observations where data_origin='REAL'"))
print("verified", cnt("select count(*) from market_observations where verification_status='MANUAL_VERIFIED'"))
print("want_null", cnt("select count(*) from market_observations where want_count is null"))
print("want_zero", cnt("select count(*) from market_observations where want_count=0"))
print("view_null", cnt("select count(*) from market_observations where view_count is null"))
print("view_nn", cnt("select count(*) from market_observations where view_count is not null"))
print("kw", cnt("select count(*) from keywords"))
print("pid", cnt("select count(*) from market_product_identities"))
print("runs", cnt("select count(*) from collection_runs"))
print("log", cnt("select count(*) from collection_log"))
print("log_by_status", list(c.execute("select status, count(*) c from collection_log group by status")))
print("products", cnt("select count(*) from products"))
print("signals", cnt("select count(*) from market_signals"))
print("sel", cnt("select count(*) from selection_results"))
print("pq", cnt("select count(*) from publish_queue"))
print("pe", cnt("select count(*) from publish_evidence"))
print("events", cnt("select count(*) from market_events"))
for r in c.execute("select id, keyword, status, total_items, valid_items, started_at, finished_at from collection_log order by id"):
    print("LOG", dict(r))
print("a949", os.path.isdir(r"D:/AI_FACTORY_OS/11_CONTENT_FACTORY/artifacts/products/a949d2e47cf1"))
con.close()
