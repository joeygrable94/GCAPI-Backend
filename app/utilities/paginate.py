def paginate(
    page: int = 1,
    limit: int = 100,
    default: int = 100,
    max: int = 10000,
) -> tuple[int, int]:  # pragma: no cover
    """A simple pagination utility.

    Args:
        page (int, optional): the page to fetch rows for. Defaults to 1.
        ppmax (int, optional): the Per Page Maximum or limit
            on how many items to return. Defaults to 100.

    Returns:
        tuple[int, int]: tuple contains a skip and limit, both integers.
        - Skip is the starting point at which the database should fetch items.
        - Limit is the total amount of items to return from the database.

    Example Input & Output:
        input   page    skip    limit
           -1     0       0       100       0-100
            0     1       0       100       0-100
            1     1       0       100       0-100
            2     2       100     100     100-200
            3     3       200     100     200-300
            4     4       300     100     300-400
    """
    if page < 1:
        page = 1
    if limit < 1:
        limit = default
    if limit > max:
        limit = max
    page = 1 if page < 1 else page
    skip: int = 0 if page == 1 else (page - 1) * limit
    return skip, limit
