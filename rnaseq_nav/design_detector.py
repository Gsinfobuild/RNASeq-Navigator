def detect_conditions(run_metadata):

    conditions = set()

    for run in run_metadata:

        title = run.get("experiment_title", "").lower()

        if ":" in title:
            condition = title.split(":")[-1].strip()
            conditions.add(condition)

    return sorted(list(conditions))
