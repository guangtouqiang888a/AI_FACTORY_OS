"""Allow: python -m database init|verify|reset"""

from database.db import main

if __name__ == "__main__":
    raise SystemExit(main())
