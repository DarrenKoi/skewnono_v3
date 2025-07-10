from datetime import datetime, date, time
from typing import Union, Dict, Optional, Tuple
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search


def parse_time_input(time_input: Union[str, datetime, date]) -> datetime:
    if isinstance(time_input, datetime):
        return time_input
    elif isinstance(time_input, date):
        return datetime.combine(time_input, time.min)
    elif isinstance(time_input, str):
        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']:
            try:
                return datetime.strptime(time_input, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse time string: {time_input}")
    else:
        raise TypeError(f"Unsupported time input type: {type(time_input)}")


def get_time_range_bounds(start: Union[str, datetime, date, None] = None,
                          end: Union[str, datetime, date, None] = None,
                          inclusive: str = 'both') -> Tuple[Optional[datetime], Optional[datetime]]:
    start_dt = parse_time_input(start) if start else None
    end_dt = parse_time_input(end) if end else None

    if end_dt and isinstance(end, (str, date)) and not isinstance(end, datetime):
        if len(str(end)) == 10 or isinstance(end, date):
            end_dt = datetime.combine(end_dt.date(), time.max)

    return start_dt, end_dt


def build_time_range_query(field: str,
                           start: Union[str, datetime, date, None] = None,
                           end: Union[str, datetime, date, None] = None,
                           inclusive: str = 'both') -> Q:
    start_dt, end_dt = get_time_range_bounds(start, end, inclusive)

    range_params = {}

    if start_dt:
        if inclusive in ['both', 'start']:
            range_params['gte'] = start_dt.isoformat()
        else:
            range_params['gt'] = start_dt.isoformat()

    if end_dt:
        if inclusive in ['both', 'end']:
            range_params['lte'] = end_dt.isoformat()
        else:
            range_params['lt'] = end_dt.isoformat()

    if not range_params:
        raise ValueError("At least one of start or end must be provided")

    return Q('range', **{field: range_params})


def search_with_time_range(es_client,
                           index: str,
                           time_field: str,
                           start: Union[str, datetime, date, None] = None,
                           end: Union[str, datetime, date, None] = None,
                           additional_filters: Optional[Dict] = None,
                           size: int = 100) -> Search:
    s = Search(using=es_client, index=index)

    time_query = build_time_range_query(time_field, start, end)
    s = s.filter(time_query)

    if additional_filters:
        for field, value in additional_filters.items():
            s = s.filter('term', **{field: value})

    s = s.params(size=size)
    s = s.sort({time_field: {'order': 'desc'}})

    return s




es = Elasticsearch(['http://localhost:9200'])

results = search_with_time_range(
    es,
    index='your_index',
    time_field='timestamp',
    start='2024-01-01',
    end='2024-01-31 23:59:59'
).execute()

results = search_with_time_range(
    es,
    index='your_index',
    time_field='created_at',
    start=datetime(2024, 1, 1, 9, 0),
    end=date(2024, 1, 31)
).execute()

results = search_with_time_range(
    es,
    index='your_index',
    time_field='updated_at',
    start='2024-01-15',
    end='2024-01-15',
    additional_filters={'status': 'active'}
).execute()