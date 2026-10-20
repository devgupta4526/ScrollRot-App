# 14 — Statistics, goals and habit feedback

## Metrics

- `today_total`: sum accepted events across supported enabled platforms for the current local date.
- `by_app_today`: accepted count by platform, including unavailable/limited confidence markers.
- `last_7_days`: one row per local date with status `observed / partial / no observations`.
- `daily_average`: defined on observable days vs all calendar days; label choice clearly.
- `goal_progress`: `(today count / goal)`, capped visually if design chooses, but keep numeric values honest.
- `time_in_apps`: optional separate permission, explicitly labeled as duration, not derived reel count.

## Charts

- XML `RecyclerView` for breakdown; custom Canvas chart or maintained view-based chart library.
- Chart accessibility description must include data in spoken list form and readable tabular fallback.
- Motion respects reduced motion; no misleading line interpolation over missing data.

## Goal rules

- User selects daily maximum exposures (e.g. 50/100/150) and can change it any time.
- Warn gently at user-defined thresholds. The mascot changes are storytelling, not measures of cognitive impairment.
- A day with tracking disabled must not be silently treated as a zero-scrolling success.
- Streaks are optional and can be hidden, paused, or reset; avoid compulsive incentive loops.

## Data tests

Daylight saving changes; travel/timezone switch; device clock manipulated; missing coverage; deleting a subset of history; app version unsupported; moving from SharedPreferences to Room with old counts; progress over 100% and goal set to 0/invalid input.
