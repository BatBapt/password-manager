import sys

import apps.interface.application as app
import apps.database.database as db


def main():
    application = app.Application()
    application.mainloop()
    sys.exit(1)


if __name__ == "__main__":
    main()
