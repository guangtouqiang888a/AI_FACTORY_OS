import sqlite3
con = sqlite3.connect(r"D:\AI_FACTORY_OS\data\ai_factory.db")
con.row_factory = sqlite3.Row
c = con.cursor()
cols = [r[1] for r in c.execute("PRAGMA table_info(market_observations)")]
needed = [
    "collection_query", "keyword_id", "want_count_status", "image_url",
    "result_position", "product_identity_id", "evidence_level",
]
print("has_foundation", all(x in cols for x in needed))
print("img", c.execute("select count(*) from market_observations where image_url is not null").fetchone()[0])
print("pos", c.execute("select count(*) from market_observations where result_position is not null").fetchone()[0])
print("kw", dict(c.execute("select id,keyword,keyword_source,discovery_class,evidence_status from keywords").fetchone()))
print("el", list(c.execute("select evidence_level, count(*) c from market_observations group by evidence_level")))
print("run", dict(c.execute("select run_id,keyword_id,collection_query,newly_accepted_count from collection_runs where run_id='crun_378745ca45e0'").fetchone()))
print("want_null", c.execute("select count(*) from market_observations where want_count is null").fetchone()[0])
print("view_null", c.execute("select count(*) from market_observations where view_count is null").fetchone()[0])
print("pid", c.execute("select count(*) from market_product_identities").fetchone()[0])
con.close()
