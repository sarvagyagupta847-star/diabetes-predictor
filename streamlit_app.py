st.subheader("What to Do Next")

if prediction == 1:

    # 🔴 HIGH RISK
    st.markdown("""
    <div class="recommend-box">
    <b>⚠️ High Risk – Recommended Actions:</b><br><br>
    • Consult a doctor immediately<br>
    • Monitor blood sugar regularly<br>
    • Reduce sugar intake<br>
    • Focus on weight management<br>
    </div>
    """, unsafe_allow_html=True)

    # 🍎 DIET TIPS
    st.subheader("🍎 Diet Tips")

    st.markdown("""
    <div class="recommend-box">
    <b>Eat:</b><br>
    • Green vegetables (spinach, broccoli)<br>
    • Whole grains (brown rice, oats)<br>
    • Protein (eggs, paneer, dal, chicken)<br>
    • Nuts and seeds<br><br>

    <b>Avoid:</b><br>
    • Sugary drinks and sweets<br>
    • Fried and junk food<br>
    • Refined carbs (maida, white bread)<br>
    </div>
    """, unsafe_allow_html=True)

    # 🏃 EXERCISE TIPS
    st.subheader("🏃 Exercise Tips")

    st.markdown("""
    <div class="recommend-box">
    • Walk at least 30 minutes daily<br>
    • Do light jogging or cycling<br>
    • Try yoga or stretching exercises<br>
    • Avoid sitting for long hours<br>
    • Do regular physical activity (5 days/week)<br>
    </div>
    """, unsafe_allow_html=True)

else:

    # 🟢 LOW RISK
    st.markdown("""
    <div class="recommend-box">
    <b>✅ Low Risk – Maintain Healthy Lifestyle:</b><br><br>
    • Continue healthy habits<br>
    • Regular exercise<br>
    • Balanced diet<br>
    </div>
    """, unsafe_allow_html=True)

    # 🍎 DIET TIPS
    st.subheader("🍎 Healthy Diet Tips")

    st.markdown("""
    <div class="recommend-box">
    • Eat fresh fruits and vegetables<br>
    • Drink enough water<br>
    • Avoid excess sugar<br>
    • Prefer home-cooked meals<br>
    </div>
    """, unsafe_allow_html=True)

    # 🏃 EXERCISE TIPS
    st.subheader("🏃 Exercise Tips")

    st.markdown("""
    <div class="recommend-box">
    • Walk 20–30 minutes daily<br>
    • Stay physically active<br>
    • Do yoga or stretching<br>
    • Avoid sedentary lifestyle<br>
    </div>
    """, unsafe_allow_html=True)
