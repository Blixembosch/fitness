"""Nutrition logic ported from the openGym fork: calorie/protein targets from body stats, a
Cronometer daily-summary parser, and the per-day consumed/remaining math. On a GLP-1 (Wegovy)
protein is the anchored number and calories never go below a floor."""
from __future__ import annotations
import io
import pandas as pd

ACTIVITY = {"sedentary": 1.2, "light": 1.4, "moderate": 1.55, "high": 1.725}


def bmr(weight_kg: float, height_cm: float, age: int, sex: str = "male") -> int:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return round(base + (-161 if sex == "female" else 5))


def estimate_targets(weight_kg, height_cm, age, sex="male", activity="light",
                     deficit=500, floor=1500, protein_per_kg=1.5, fat_pct=0.30, kcal=None) -> dict:
    """TDEE from Mifflin-St Jeor × activity. `kcal` fixes the calorie goal directly (a manual
    target); otherwise it's TDEE − deficit, floored. Returns tdee, kcal, protein/carbs/fat and the
    implied daily deficit vs TDEE (negative = surplus)."""
    tdee = round(bmr(weight_kg, height_cm, age, sex) * ACTIVITY.get(activity, ACTIVITY["light"]))
    kcal = round(kcal / 10) * 10 if kcal else max(floor, round((tdee - deficit) / 10) * 10)
    protein = round(protein_per_kg * weight_kg)
    fat = round(kcal * fat_pct / 9)
    carbs = max(0, round((kcal - protein * 4 - fat * 9) / 4))
    return {"tdee": tdee, "kcal": kcal, "protein": protein, "carbs": carbs, "fat": fat,
            "deficit": tdee - kcal}


def weekly_loss(deficit_kcal) -> float:
    """Approx kg/week from a daily kcal deficit (~7700 kcal per kg of fat)."""
    return round((deficit_kcal or 0) * 7 / 7700, 2)


def bmi(weight_kg: float, height_cm: float):
    return round(weight_kg / (height_cm / 100) ** 2, 1) if height_cm else None


def adjusted_weight(weight_kg: float, height_cm: float) -> float:
    """Adjusted body weight for protein calculation when BMI > 25 (Helms / Examine GLP-1 guidance).
    Prevents over-prescribing protein on raw fat mass while fully protecting lean mass."""
    if not height_cm or not weight_kg:
        return float(weight_kg or 100.0)
    ref_w = 25.0 * (height_cm / 100.0) ** 2
    if weight_kg <= ref_w:
        return round(float(weight_kg), 1)
    return round(ref_w + 0.40 * (weight_kg - ref_w), 1)


def protein_band(weight_kg: float, height_cm: float, mode: str = "adjusted") -> dict:
    """Return {'target': int, 'min': int, 'max': int, 'eff_weight': float, 'mode': str}.
    - 'adjusted' (default for Wegovy): uses adjusted body weight (~160 g target, 150–181 g band at 100.5 kg / 178 cm).
    - 'strict': uses raw total weight × 1.8 g/kg (~181 g target, 161–201 g band).
    """
    w = float(weight_kg or 100.0)
    adj = adjusted_weight(w, height_cm or 178)
    if mode == "strict":
        tgt = round(w * 1.8)
        lo = round(w * 1.6)
        hi = round(w * 2.0)
        return {"target": tgt, "min": lo, "max": hi, "eff_weight": round(w, 1), "mode": "strict"}
    lo = max(120, round(adj * 1.7 / 5) * 5)
    tgt = max(lo, round(adj * 1.85 / 5) * 5)
    hi = max(tgt, round(w * 1.8))
    return {"target": tgt, "min": lo, "max": hi, "eff_weight": adj, "mode": "adjusted"}


# --- Cronometer dailysummary.csv -> tidy frame [date, kcal, protein, carbs, fat, fiber] ---
_COLS = {
    "kcal": ["energy (kcal)", "energy", "calories", "kcal"],
    "protein": ["protein (g)", "protein"],
    "carbs": ["carbs (g)", "net carbs (g)", "carbohydrates (g)", "carbs"],
    "fat": ["fat (g)", "fat"],
    "fiber": ["fiber (g)", "fibre (g)", "fiber"],
}


def _find(colmap: dict[str, str], names: list[str]):
    for n in names:
        if n in colmap:
            return colmap[n]
    return None


def parse_cronometer(file) -> pd.DataFrame:
    """Accepts a file-like or bytes of Cronometer's dailysummary.csv. Returns one row per day.

    Cronometer exports rows per meal (Group = Breakfast/Lunch/…) plus a daily `Total` row. We keep
    ONLY the Total rows so nutrients aren't double-counted; if there's no Group column (older export
    format with one row per day) we take every row. Empty days (no entries) are dropped.
    """
    raw = file.read() if hasattr(file, "read") else file
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig", errors="replace")
    df = pd.read_csv(io.StringIO(raw))
    colmap = {c.strip().lower(): c for c in df.columns}
    date_col = _find(colmap, ["date", "day"])
    if not date_col:
        raise ValueError("Tarih sütunu bulunamadı (Date).")
    group_col = _find(colmap, ["group", "category"])
    if group_col:
        df = df[df[group_col].astype(str).str.strip().str.lower() == "total"]
    out = pd.DataFrame()
    out["date"] = pd.to_datetime(df[date_col], errors="coerce").dt.strftime("%Y-%m-%d")
    for key, names in _COLS.items():
        src = _find(colmap, names)
        out[key] = pd.to_numeric(df[src], errors="coerce") if src else 0.0
    out = out.dropna(subset=["date"])
    # one row per day; drop days with no real intake logged
    out = out.groupby("date", as_index=False).sum(numeric_only=True).round(1)
    out = out[out["kcal"] > 0].sort_values("date").reset_index(drop=True)
    return out


def day_summary(entry: dict, targets: dict) -> dict:
    out = {}
    for k in ("kcal", "protein", "carbs", "fat"):
        consumed = float(entry.get(k) or 0)
        target = targets.get(k)
        out[k] = {
            "consumed": round(consumed, 1),
            "target": target,
            "remaining": round(target - consumed, 1) if target else None,
            "pct": round(consumed / target * 100) if target else None,
        }
    return out


def protein_adherence(days: pd.DataFrame, protein_target: float) -> dict:
    if days is None or days.empty:
        return {"days": 0, "met": 0, "avg_protein": 0, "avg_kcal": 0}
    return {
        "days": len(days),
        "met": int((days["protein"] >= protein_target).sum()) if protein_target else 0,
        "avg_protein": round(days["protein"].mean()),
        "avg_kcal": round(days["kcal"].mean()),
    }


def upsert_day(
    df: pd.DataFrame | None,
    date_str: str,
    kcal: float,
    protein: float,
    carbs: float,
    fat: float,
    fiber: float,
) -> pd.DataFrame:
    """Insert or update a single day's nutrition row in the nutrition DataFrame."""
    row = {
        "date": str(date_str),
        "kcal": round(float(kcal), 1),
        "protein": round(float(protein), 1),
        "carbs": round(float(carbs), 1),
        "fat": round(float(fat), 1),
        "fiber": round(float(fiber), 1),
    }
    cols = ["date", "kcal", "protein", "carbs", "fat", "fiber"]
    if df is None or df.empty:
        return pd.DataFrame([row], columns=cols)
    new_df = df.copy()
    for col in cols:
        if col not in new_df.columns:
            new_df[col] = 0.0
    if date_str in new_df["date"].values:
        idx = new_df.index[new_df["date"] == date_str][0]
        for k, v in row.items():
            new_df.at[idx, k] = v
    else:
        new_df = pd.concat([new_df, pd.DataFrame([row])], ignore_index=True)
    return new_df.sort_values("date").reset_index(drop=True)


def remove_day(df: pd.DataFrame | None, date_str: str) -> pd.DataFrame:
    """Remove a day's nutrition record from the DataFrame."""
    cols = ["date", "kcal", "protein", "carbs", "fat", "fiber"]
    if df is None or df.empty:
        return pd.DataFrame(columns=cols)
    new_df = df[df["date"] != str(date_str)].copy()
    return new_df.sort_values("date").reset_index(drop=True)


def merge_nutrition(base_df: pd.DataFrame | None, new_df: pd.DataFrame | None) -> pd.DataFrame:
    """Merge two nutrition DataFrames, updating rows by date and sorting chronologically."""
    cols = ["date", "kcal", "protein", "carbs", "fat", "fiber"]
    if base_df is None or base_df.empty:
        return new_df if (new_df is not None and not new_df.empty) else pd.DataFrame(columns=cols)
    if new_df is None or new_df.empty:
        return base_df
    combined = pd.concat([base_df, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=["date"], keep="last")
    return combined.sort_values("date").reset_index(drop=True)


def generate_cronometer_csv(df: pd.DataFrame | None) -> str:
    """Export nutrition records to Cronometer-compatible dailysummary.csv format."""
    header = "Date,Energy (kcal),Protein (g),Net Carbs (g),Fat (g),Fiber (g),Group\n"
    if df is None or df.empty:
        return header
    lines = [header]
    for _, r in df.sort_values("date").iterrows():
        d = str(r["date"])
        kc = round(float(r.get("kcal", 0)), 1)
        p = round(float(r.get("protein", 0)), 1)
        c = round(float(r.get("carbs", 0)), 1)
        f = round(float(r.get("fat", 0)), 1)
        fib = round(float(r.get("fiber", 0)), 1)
        lines.append(f"{d},{kc},{p},{c},{f},{fib},Total\n")
    return "".join(lines)
