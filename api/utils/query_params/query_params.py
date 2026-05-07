from django.db.models import Q
from datetime import datetime

def infer_type(value: str):
    if value.lower() in ["true", "false"]:
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    try:
        parsed_date = datetime.fromisoformat(value)
        return parsed_date
    except ValueError:
        pass
    return value

def parse_condition(condition: str, lookup_delimiter: str = "||") -> dict:
    field, operator, value = condition.split(lookup_delimiter)
    parsed_value = infer_type(value)

    lookup = ""
    if operator in ["$eq", "=", "=="]:
        lookup = field
    elif operator in ["!", "$ne"]:
        lookup = f"{field}__ne"
    elif operator in ["$cont"]:
        lookup = f"{field}__icontains"
    elif operator in ["$isnull"]:
        lookup = f"{field}__isnull"
    elif operator in ["$gt"]:
        lookup = f"{field}__gt"
    elif operator in ["$gte"]:
        lookup = f"{field}__gte"
    elif operator in ["$lt"]:
        lookup = f"{field}__lt"
    elif operator in ["$lte"]:
        lookup = f"{field}__lte"
    elif operator in ["$starts"]:
        lookup = f"{field}__istartswith"
    elif operator in ["$ends"]:
        lookup = f"{field}__iendswith"
    elif operator in ["$in"]:
        parsed_value = [infer_type(v) for v in value.split(",")]
        lookup = f"{field}__in"
    elif operator in ["$between"]:
        start, end = value.split(",")
        return {
            f"{field}__gte": infer_type(start),
            f"{field}__lte": infer_type(end),
        }
    else:
        lookup = field

    return {lookup: parsed_value}


def parse_filters(
    filter_string: str = None,
    search: str = None,
    searchable_fields: list = None,
    lookup_delimiter: str = "||"
):
    query = Q()

    if filter_string:
        tokens = filter_string.split(";")

        inside_parentheses = False
        temp_group = []

        for token in tokens:
            token = token.strip()

            if token.startswith("("):
                inside_parentheses = True
                token = token[1:]  # remove starting '('
                temp_group.append(token)
            elif token.endswith(")"):
                token = token[:-1]  # remove ending ')'
                temp_group.append(token)

                # group finished, build OR query
                or_query = Q()
                for cond in temp_group:
                    parsed = parse_condition(cond, lookup_delimiter)
                    or_query |= Q(**parsed)
                query &= or_query

                inside_parentheses = False
                temp_group = []
            elif inside_parentheses:
                temp_group.append(token)
            else:
                parsed = parse_condition(token, lookup_delimiter)
                query &= Q(**parsed)

    if search and searchable_fields:
        search_query = Q()
        for field in searchable_fields:
            search_query |= Q(**{f"{field}__icontains": search})
        query &= search_query

    return query

def parse_sort(sort: str = None) -> list:
    if not sort:
        return []

    sort_fields = sort.split(";")
    order_by_fields = []

    for field in sort_fields:
        parts = field.split(":")
        if len(parts) == 2:
            field_name, direction = parts
            direction = direction.lower()
            if direction == "desc":
                order_by_fields.append(f"-{field_name.strip()}")
            else:
                order_by_fields.append(field_name.strip())
        else:
            # default ascending if no direction provided
            order_by_fields.append(parts[0].strip())

    return order_by_fields