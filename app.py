import json
import streamlit as st

def mock_call_llm(payload: dict) -> dict:
    brand = payload.get("brand_name", "").strip() or "Your Brand"
    tone = payload.get("tone", "Professional").strip()
    product = payload.get("product", "").strip()
    avoid = [w.strip().lower() for w in payload.get("avoid_words", "").split(",") if w.strip()]
    n = int(payload.get("n", 5))

    tone_styles = {
        "Professional": ["Precision", "Trusted", "Built", "Crafted", "Clear"],
        "Playful": ["Spark", "Pop", "Bright", "Fun", "Zing"],
        "Bold": ["Own", "Lead", "Unmissable", "Power", "Break"],
        "Minimal": ["Simply", "Less", "Pure", "Just", "Only"],
        "Friendly": ["Hello", "Together", "Easy", "Kind", "Welcome"],
    }
    words = tone_styles.get(tone, tone_styles["Professional"])

    candidates = [
        f"{words[0]} ideas. {brand} results.",
        f"{brand}: {words[1]} brand voice, faster.",
        f"Stay on-brand. Say it better with {brand}.",
        f"{words[2]} for {product or 'your product'}.",
        f"{brand} makes your message {words[3].lower()}.",
        f"{words[4]} slogans. Consistent brand. Less effort.",
        f"From brand brief to slogan—{brand} delivers.",
    ]

    def is_ok(s: str) -> bool:
        s_low = s.lower()
        return all(bad not in s_low for bad in avoid)

    slogans = []
    for s in candidates:
        if is_ok(s):
            slogans.append(s)
        if len(slogans) >= n:
            break

    if not slogans:
        slogans = [f"{brand}: On-brand messaging, made simple."][:n]

    return {
        "slogans": [{"text": s, "rationale": f"Matches a {tone.lower()} tone and uses only provided inputs."} for s in slogans],
        "consistency_checklist": [
            f"Kept a {tone.lower()} tone across options",
            "Used only information from the brand inputs (no extra claims)",
            "Short, punchy slogans (<= 10 words)"
        ],
        "disclaimer": "Demo mode (no API). Outputs are illustrative; human review recommended."
    }

st.set_page_config(page_title="BrandSpark MVP", layout="wide")
st.title("BrandSpark MVP – Brand-Consistent Slogan Generator (Demo)")

st.caption("Demo mode – no API used.")

colA, colB = st.columns(2)

with colA:
    brand_name = st.text_input("Brand name")
    product = st.text_input("Product / Service")
    audience = st.text_input("Target audience")
    value_prop = st.text_input("Value proposition")
    features = st.text_area("Key features (comma separated)")
    tone = st.selectbox("Tone of voice", ["Professional", "Playful", "Bold", "Minimal", "Friendly"])
    avoid_words = st.text_input("Words to avoid (comma separated)")
    n = st.slider("Number of slogans", 1, 7, 3)

if st.button("Generate"):
    payload = {
        "brand_name": brand_name,
        "product": product,
        "audience": audience,
        "value_prop": value_prop,
        "features": features,
        "tone": tone,
        "avoid_words": avoid_words,
        "n": n,
    }

    result = mock_call_llm(payload)

    with colB:
        st.subheader("Slogans")
        for i, item in enumerate(result["slogans"], 1):
            st.markdown(f"**{i}. {item['text']}**")
            st.write(item["rationale"])

        st.subheader("Brand consistency checklist")
        for b in result["consistency_checklist"]:
            st.write(f"- {b}")

        st.info(result["disclaimer"])
