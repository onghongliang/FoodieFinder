def sequential_search(data, search_term):
    matched_records = []
    for record in data:
        if search_term.lower() in str(record['Title']).lower():
            matched_records.append(record)
    return matched_records
